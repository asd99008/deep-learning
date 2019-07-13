


def zero_pad(image, pad_height, pad_width):
    """ Zero-pad an image.

  

    H, W = image.shape
    out = None

    # YOUR CODE HERE
    out = np.pad(image, ((pad_height, pad_height), (pad_width,
                                                    pad_width)), 'constant', constant_values=(0, 0))
    pass
    # END YOUR CODE
    return out

def replica_pad(image, pad_height, pad_width):

    H, W = image.shape
    out = None

    # YOUR CODE HERE
    out = np.pad(image, ((pad_height, pad_height), (pad_width,
                                                    pad_width)), 'constant', constant_values=(image[0][0],image[H-1][W-1]))
    pass
    # END YOUR CODE
    return out



def conv_fast(image, kernel,padding_way):
   
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    if padding_way  = 'zero':
        image = zero_pad(image, Hk - 1, Wk - 1)
    elif padding_way     = 'replica':
        image = replica_pad (image, Hk - 1, Wk - 1)
    
    kernel = np.fliplr(kernel)
    kernel = np.flipud(kernel)
    out1 = np.zeros((Hi + Hk - 1, Wi + Wk - 1))
    for i in range(0, Hi + Hk - 1):
        for j in range(0, Wi + Wk - 1):
            temp = 0.0
            for m in range(0, Hk):
                for n in range(0, Wk):
                    temp += kernel[m][n] * image[m + i][n + j]
            out1[i][j] = temp

    for i in range(0, Hi):
        for j in range(0, Wi):
            out[i][j] = out1[i + (Hk - 1) / 2][j + (Wk - 1) / 2]
            pass
        pass
    pass
    # END YOUR CODE

    return out
