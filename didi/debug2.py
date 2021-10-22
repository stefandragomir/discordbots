import rowordnet


wn = rowordnet.RoWordNet()

word = 'arbore'
synset_ids = wn.synsets(literal=word)
print("Total number of synsets containing literal '{}': {}".format(word, len(synset_ids)))
print(synset_ids)