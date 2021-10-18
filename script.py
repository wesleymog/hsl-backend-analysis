import json
def get_dataset():
    with open('teste.json') as json_file:
        data = json.load(json_file)
        clinicas = data['clinicas'][:10]
        labels =[]
        data_set = []
        for clinica in clinicas:
            if clinica['clinica'] not in labels:
                labels.append(clinica['clinica'])
        for clinica in clinicas:
            if not any(d['label'] == clinica['nome_exame'] for d in data_set):
                dict_ ={}
                dict_['label'] = clinica['nome_exame']
                dict_['data'] = [0 for _ in range(len(labels))]
                dict_['data'][labels.index(clinica['clinica'])]=clinica['quantidade']
                data_set.append(dict_)
            else:
                for d in data_set:
                    if d['label'] == clinica['nome_exame']:
                        d['data'][labels.index(clinica['clinica'])]=clinica['quantidade']
    return {"labels": labels, "datasets":data_set}

                
print(get_dataset())
print(len(get_dataset()['datasets']))
print(len(get_dataset()['labels']))