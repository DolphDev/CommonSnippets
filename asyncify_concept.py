import asyncio
import concurrent.futures

# Concept
# Make anything IO asyncable
# Could used cleanup

# probably doesn't need to be a class
class Wrapper:
	def __init__(self, func):
		self.func = func 

	async def __aenter__(self, *args):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			job = executor.submit(self.func)
			while not job.done():
				await asyncio.sleep(0.1)
			self.result = job.result()

	async def __aexit__(self, *args):
		await asyncio.sleep(0)

def asyncify(function):
	async def f():
		job = Wrapper(function)
		async with job:
			pass
		return job.result
	return f
