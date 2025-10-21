options(repos = c(CRAN = "https://cloud.r-project.org"))

install.packages(c("nycflights13",  "gapminder", "RColorBrewer",
                    "gganimate","emmeans","mgcv","nlme","broom",
                    "tidybayes","maps","statebins","sf","maptools",
                    "sp","rgeos","ggspatial","geofacet","misc3d",
                    "plot3D","magick","hexbin","treemapify",
                    "gridExtra", "rworldmap","ggmap","ggthemes",
                    "ggfortify","ggridges","ggrepel","ggforce",
                    "patchwork","lubridate","forcats","stringr",
                    "purrr","readr","tidyr","tibble","tidyverse",
                    "dplyr","ggplot2","colorspace","rjson","class",
                    "rprojroot","estimability","ggstance","rstudioapi",
                    "farver","ggfittext","svUnit","mvtnorm","xml2",
                    "knitr", "polyclip","jsonlite","png","pngjsonlite",
                    "httr", "backports", "assertthat","Matrix","lazyeval",
                    "cli","tweenr","prettyunits","htmltools",
                    "htmlwidgets","coda","gtable","glue","Rcpp",
                    "cellranger","imguR","xfun","rvest","MASS",
                    "scales","hms","yaml","stringi","e1071","spData",
                    "RgoogleMaps", "rlang","pkgconfig","bitops",
                    "geogrid","evaluate","lattice","tidyselect","plyr",
                    "magrittr","R6", "generics","DBI","pillar","haven",
                    "foreign","withr","units","modelr","crayon",
                    "arrayhelpers", "progress","jpeg","rnaturalearth",
                    "readxl","digest","classInt", "xtable", "munsell",
                    "ggplot2movies", "base64enc","rmarkdown", 
                    "tikzDevice","scales","bookdown","remotes",
                    "FactoMineR","tidymodels","vcd"," lwgeom",
                    "gridGraphics","caret", "repr", "GGally",
                    "IRdisplay", "pdbZMQ", "argparse", "reticulate"))

remotes::install_github("rijksuniversiteit-groningen/cds-utils",subdir="rugutils")
remotes::install_github("rijksuniversiteit-groningen/rugplot@venus/feature/schemarefs")
remotes::install_github('wilkelab/cowplot')
remotes::install_github('clauswilke/colorblindr')
remotes::install_github('clauswilke/dviz.supp')
remotes::install_github('wilkelab/ungeviz')
remotes::install_github('clauswilke/ggtextures')
remotes::install_github('DavisVaughan/strapgod')
remotes::install_github('ropensci/plotly')
remotes::install_github('ropensci/jsonvalidate')
remotes::install_github("thomasp85/transformr")
