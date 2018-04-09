from ...adapter import better_bench_cpu, better_bench_gpu

def check_cpu(cpu_filter):

    return better_bench_cpu(cpu_filter)


def check_gpu(gpu_filter):

	return better_bench_gpu(gpu_filter)