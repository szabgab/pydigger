from pydigger.implementation import PyDigger
statuses = (
	('waiting_for_zip_url',          'The first status after a package is added to the database, as it seems there might be a delay updating the JSON file on PyPi.'),
	('error_unknown_zip_file_type',  'The zip file listed in the JSON file is in a format PyDigger does not handle yet. Currently supported formats are .zip and .tag.gz.'),
	('zip_url_found',                'A zip URL found in the JSON file. (Currently this is the final state as well.)'),
	('error_unknown_zip_url_prefix', 'Sanity check that the zip file is being donwloaded from https://pypi.python.org/'),
)
def get_statuses():
	return [s[0] for s in statuses]
