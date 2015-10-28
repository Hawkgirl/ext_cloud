from BaseCloud.BaseStats.BaseStats import BaseStatscls

class OpenStackMetricscls(BaseStatscls):

	def __init__(self, *arg, **kwargs):
                super(OpenStackMetricscls, self).__init__(*args,**kwargs)

	def list_metrics(self):
		metrics = []
		return metrics

