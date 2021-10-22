import rowordnet


_net = rowordnet.RoWordNet()

_ids = _net.synsets(literal='casa')


for _id in _ids:

	print(_id)
	_object = _net.synset(_id)

	print(_object.literals)