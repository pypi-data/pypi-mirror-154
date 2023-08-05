from captum.attr import Saliency

import torch

class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        self.model.eval()
        self.explain=Saliency(model)


    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        attributions = self.explain.attribute(img, target=target,abs=False)
        return torch.abs(attributions)
        #return attributions
