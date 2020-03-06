# Libraries
library(ggplot2)
library(hrbrthemes)
library(dplyr)
library(tidyr)
library(viridis)
library(tidyverse)

# The diamonds dataset is natively available with R.
train <- read.csv("../../datasets/train_clean.csv")


p2 <- ggplot(data = train, aes(x = year_built,group = overall_qual, fill =yr_sold, alpha=0.5)) +
  geom_density(adjust = 1.5) 

p2 + scale_x_continuous(labels = function(x) format(x, scientific = FALSE)) +
  scale_y_continuous(labels = function(x) format(x, scientific = FALSE)) + 
  ggtitle("Distribution of Sale Prices and Overall Quality") + scale_color_gradient2()


# Using Small multiple
ggplot(data=train, aes(x=saleprice, group=neighborhood, fill=price_per_sqft)) +
  geom_density(adjust=1.5) + scale_colour_gradient2() + 
  facet_wrap(~neighborhood) +
  theme(
    legend.position="none",
    panel.spacing = unit(0.5, "lines"),
    axis.ticks.x=element_blank()
  ) + scale_x_continuous(labels = function(x) format(x, scientific = FALSE)) +
scale_y_continuous(labels = function(x) format(x, scientific = FALSE)) 





