import paddle


path1 = "./output/PPLCNet_x0_25/epoch_1.pdparams"
#path2 = "./output/PPLCNet_x0_25/epoch_2.pdparams"
path2 = "/root/.paddleclas/weights/PPLCNet_x0_25_pretrained.pdparams"

state1 = paddle.load(path1)
state2 = paddle.load(path2)

for k in state1:
    if not (state1[k].numpy()==state2[k].numpy()).all():
        print(k)
