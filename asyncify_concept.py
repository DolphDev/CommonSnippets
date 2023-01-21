import asyncio
import concurrent.futures

# Concept
# Make anything IO asyncable. 
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


# Class isn't needed

def asyncify(function):
    async def wrapped(*args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            job = executor.submit(function, *args, **kwargs)
            while not job.done():
                await asyncio.sleep(0.05)
            return job.result()
    return wrapped


# If you don't mine getting the event loop
def asyncify(func):
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper
