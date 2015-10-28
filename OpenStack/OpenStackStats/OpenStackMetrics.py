from BaseCloud.BaseStats.BaseStats import BaseStatscls

class OpenStackMetricscls(BaseStatscls):

	def __init__(self, *arg, **kwargs):
                super(BaseStatscls, self).__init__(*args,**kwargs)

	def get_metrics(self):
		metrics = []
		return metrics

