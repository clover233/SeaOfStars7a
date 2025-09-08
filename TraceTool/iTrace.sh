#!/bin/zsh
capture_time=10
while ((i<2))
do
  time=$(date +%Y%m%d_%H%M%S)
  trace_name="${time}(${capture_time}s).trace"
  cmd="xctrace record --template 'UX-HitchAndMetal' --all-processes --output '${trace_name}'  --device-name 'iPhone (17.2)' --time-limit ${capture_time}s"
  eval $cmd
  let i++
done