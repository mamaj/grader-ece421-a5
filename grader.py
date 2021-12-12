import numpy as np
import pandas as pd
from tqdm.notebook import tqdm, trange
import nbutils
from pathlib import Path



def get_between(nb, clue):

    result = []
    cell_iterator = iter(nb['cells'])
    
    for cell in cell_iterator:
        
        if ismd(cell) and clue[0] in cell['source']:
            result.append(cell['source'].split(clue[0])[1])
            for cell in cell_iterator:
                if ismd(cell) and clue[1] in cell['source']:
                    return result
                elif ismd(cell):
                    result.append(cell['source'])
    
    return result

    
    
def ismd(cell):
    return cell['cell_type'] == 'markdown'


clue = [
    '**Questions 7** (bonus)[5 points]: With an example, explain in detail what does lax.scan function do, and what it is useful for?',
    '# The classifier'
]


df = pd.read_csv('./Assignment 5 - Sheet1.csv').fillna('')
df['sol'] = np.nan

for i, stdid in df['ID'].iteritems():
    files = list(Path('subs').glob(f'*_{stdid}_*.ipynb'))
    if len(files) == 1:
        nb = nbutils.read_nb(files[0])
        sol = '\n'.join(get_between(nb, clue))
        df.loc[i, 'sol'] = sol

print(df)
df.to_csv('sol.csv', index=False)


