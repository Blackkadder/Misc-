library(igraph)
library(extrafont)
library(readr)

map1 <- read_csv("C:/Users/e115487/Box Sync/Revenue deep dive/explore/map1.csv")


net <- graph.data.frame(map1, directed=T)

plot(net)

net <- simplify(net, remove.multiple = F, remove.loops = T) 
plot(net, edge.arrow.size=.4)

plot(net, vertex.size=30)

plot(net, edge.arrow.size=.2,vertex.shape="none", vertex.label.family="Arial Black",
     edge.curved=.1,vertex.color="gray", edge.color = "blue",vertex.label.color="black",
     vertex.frame.color = 'gray', vertex.label.font=0.5)


l <- layout_with_kk(net)

plot(net, vertex.shape="none", 
     vertex.label.font=2, vertex.label.color="black",
     vertex.label.cex=1.5,edge.color=c("gray50", "orange")[(E(net)$type=="Primary")+1],
     edge.arrow.size=.4,layout=layout_as_star(net))

