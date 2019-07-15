import numpy as np
import random
import matplotlib.pyplot as plt

def inference(w,b,x):
    pred_y = np.dot(w,x)+b
    return pred_y
    
def eval_loss(w, b, x, gt_y):
    inner = (np.dot(w,x)-gt_y)**2
    return np.sum(inner)/(2*len(x))
    
def gradient(pred_y, gt_y, x):
    diff = pred_y - gt_y
    dw = np.dot(diff, x)
    db = diff
    return dw,db
    
def cal_step_gradient(batch_x_list,batch_gt_y_list,w,b,lr):
    avg_dw, avg_db = 0, 0
    batch_size = len(batch_x_list)
    
    pred_y = inference(w,b,batch_gt_y_list)
    dw,db = gradient(pred_y,batch_gt_y_list,batch_x_list)
    avg_dw = np.sum(dw) / batch_size
    avg_db = np.sum(db) / batch_size
    w -= lr * avg_dw
    b -= lr * avg_db
    return w,b
    
def train(x_list, gt_y_list, batch_size, lr, max_iter):
    w = 0
    b = 0
    num_samples = len(x_list)
    
    for i in range(max_iter):
        batch_idxs = np.random.choice(len(x_list), batch_size)
        batch_x = [x_list[j] for j in batch_idxs]
        batch_y = [gt_y_list[j] for j in batch_idxs]
        w, b = cal_step_gradient(batch_x, batch_y, w, b, lr)
        print('w:{0}, b:{1}'.format(w, b))
        print('loss is {0}'.format(eval_loss(w, b, x_list, gt_y_list)))
        
  def gen_sample_data():
    w = random.randint(0, 10) + random.random()		# for noise random.random[0, 1)
    b = random.randint(0, 5) + random.random()
    num_samples = 100
    x_list = []
    y_list = []
    
    for i in range(num_samples):
        x = random.randint(0, 100) * random.random()
        y = w * x + b + random.random() * random.randint(-1, 1)
        x_list.append(x)
        y_list.append(y)
    return x_list, y_list, w, b
    
 def run():
    x_list, y_list, w, b = gen_sample_data()
    plt.scatter(x_list, y_list)
    x = np.linspace(0,100,100)
    lr = 0.001
    max_iter = 1000
    train(x_list, y_list, 50, lr, max_iter)
    plt.plot(x,x*w+b,'r',lw = 4)
    plt.show()
