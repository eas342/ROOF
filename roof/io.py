import os
from astropy.io import fits

class Data:
	'''
	A simple class to hold data
	'''

	def __init__(self, filepath, **kwargs):
		# Assign the filepath to the data
		self.filepath = filepath

		# Load the data from the filepath
		self.load_data(filepath)


	def load_data(self, filepath):
		'''
		Function to load JWST pipeline data prior to ramp fitting
		'''
		# Check if filepath is actually a file
		if not os.path.isfile(filepath):
			raise ValueError('File path not recognised as a file.')

		# Open FITS file
		with fits.open(filepath) as hdul:
			self.phead = hdul[0].header
			self.sci = hdul['SCI'].data
			self.pixdq = hdul['PIXELDQ'].data
			self.grpdq = hdul['GROUPDQ'].data
			self.err = hdul['ERR'].data

		return

	def finish_stage1(self, output_dir):

		# Putting this import here for now...
		from jwst.pipeline.calwebb_detector1 import Detector1Pipeline

		pipeline = Detector1Pipeline()
		# Skip steps that should already be done
		pipeline.group_scale.skip = True
		pipeline.dq_init.skip = True
		pipeline.saturation.skip = True
		pipeline.ipc.skip = True
		pipeline.superbias.skip = True
		# Persistence step is also skipped for TSO observations
		pipeline.persistence.skip = True

		pipeline.save_results = True
		pipeline.output_dir = output_dir
		pipeline.run(self.filepath)

		return


	# Power spectrum

	# ABC method

	# Median method

	# Polynomial fit method