using Distributions

N    = 500
dist = Erlang(7,0.5)
draw = rand(dist,N)

hist(draw)