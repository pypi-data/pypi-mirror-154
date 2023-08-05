# Load functions
from scipy.stats.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import seaborn as sns
from collections import defaultdict
import scipy
from scipy import stats
from statsmodels.stats.multitest import multipletests
from functools import reduce
import umap

import matplotlib
import matplotlib.pyplot as plt
import random
import copy
import scipy
from scipy import stats
matplotlib.use('agg')
plt.style.use('seaborn-whitegrid')

import warnings
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator

import os, sys
import torch
import numpy as np
from torch.utils import data
import re 

from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data.dataset import TensorDataset
import plot_importance
from tqdm import tqdm


from move._utils.data_utils import *
from move._utils.visualization_utils import embedding_plot_discrete, embedding_plot_float, visualize_training, plot_reconstruction_distribs, visualize_embedding, plot_categorical_importance, plot_continuous_importance
from move._training.train import train_model_latent
from move._analysis.analysis import *

import hydra 
from move.conf.schema import MOVEConfig
from move._utils.data_utils import get_data
import move.VAE_v2_1

# # Load MOVE specific funtions and SHAP analysis
# path = "./"
# sys.path.append(path + "src/")

# import plot_importance

# data_dict = read_yaml('data')
# cat_list, con_list, cat_names, con_names, headers_all, drug, drug_h = get_data(data_dict)


# # Set to True if training using a GPU
# cuda = False

# # Training parameters
# nepochs=2 # Changed from nepochs=200
# lrate=0.0001
# kldsteps=[20, 30, 40]
# batchsteps=[50, 100, 150, 200]
# # optimizer = optim.Adam(model.parameters(), lr=lrate)

# epochs = range(1, nepochs + 1)


# #nepochs from earlier training



@hydra.main(config_path="../conf", config_name="main")
def main(config: MOVEConfig): 
        # By cosine similirity. 
    
    #Get needed variables
    cuda = config.training.cuda
    path = config.data.processed_data_path
    nHiddens = config.model.num_hidden
    nLatents = config.model.nLantent_04
    nLayers = config.model.num_layers
    nDropout = config.model.dropout
    nBeta = config.model.beta
    batch_sizes = config.model.batch_sizes
    nepochs = config.training.num_epochs
    repeat = config.training.repeat
    lrate = config.training.lr
    kld_steps = config.training.kld_steps
    batch_steps = config.training.batch_steps
    patience = config.training.patience
    path = config.data.processed_data_path
    categorical_names = config.model.categorical_names
    continuous_names = config.model.continuous_names
    data_of_interest = config.data.data_of_interest
    
    epochs = range(1, nepochs + 1)
    #Get the data
    cat_list, con_list, cat_names, con_names, headers_all, drug, drug_h = get_data(path, categorical_names, continuous_names, data_of_interest)
        
        
    best_model, mask, train_loader, losses, ce, sse, KLD, cat_shapes, con_shapes = train_model_latent(path, cuda, nepochs, kld_steps, batch_steps, lrate, con_list, cat_list, nHiddens, nLatents, nLayers, nBeta, nDropout)
    
    visualize_training(losses, ce, sse, KLD, epochs)
    
    latent, latent_var, cat_recon, cat_class, con_recon, loss, likelihood = get_latents(best_model, train_loader, 1)
    
    cat_total_recon = calc_categorical_reconstruction_acc(cat_shapes, cat_class, cat_recon)
    
    all_values = calc_continuous_reconstruction_acc(con_shapes, con_recon, train_loader)
    
    plot_reconstruction_distribs(cat_total_recon, all_values)
    
    embedding = get_embedding(path, latent)
    
    visualize_embedding('categorical', "drug_1", embedding, 
                    mask, cat_list, con_list, cat_names, con_names)
    # visualize_embedding('continuous', "clinical_continuous_1", embedding,  #Todo: clinical_continuous_1 does not exist??
    #                     mask, cat_list, con_list, cat_names, con_names)
    visualize_embedding('continuous', "clinical_continuous_2", embedding, 
                        mask, cat_list, con_list, cat_names, con_names)    
     
    
    
    get_pearsonr('categorical', "drug_1", embedding, cat_list, con_list, cat_names, con_names)
    get_pearsonr('continuous', "clinical_continuous_2", embedding, cat_list, con_list, cat_names, con_names)
    
    
    all_diffs, all_diffs_cat_np, sum_diffs_cat_np, sum_diffs_cat_abs_np,\
        total_diffs_cat_np = get_feature_importance_categorical(best_model, train_loader, latent)

    
    all_diffs_con_np, sum_diffs_con_np, sum_diffs_con_abs_np,\
            total_diffs_con_np = get_feature_importance_continuous(best_model, train_loader, mask, latent)

    save_feat_results(path, all_diffs_cat_np, sum_diffs_cat_np, sum_diffs_cat_abs_np, total_diffs_cat_np, 
                 all_diffs_con_np, sum_diffs_con_np,sum_diffs_con_abs_np, total_diffs_con_np)
    
    
    plot_categorical_importance(path=path,
                            sum_diffs=sum_diffs_cat_np,
                            cat_list=cat_list,
                            feature_names=cat_names,
                            fig_name='importance_SHAP_cat')
    
    
    plot_continuous_importance(path=path,
                           train_loader=train_loader,
                           sum_diffs=sum_diffs_con_np,
                           feature_names=con_names,
                           fig_name='importance_SHAP_c')
    
    
    get_feat_importance_on_weights(path, best_model, train_loader, cat_names, con_names)


if __name__ == "__main__":
    main()
