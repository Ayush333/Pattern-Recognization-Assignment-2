from mpmath import mpf, mpc, mp

def main():
	mp.dps=100
	total=mpf(0)
	total+=mpf(1.4386767659979371e-41)
	total+=mpf(6.645073526610289e-05)
	total+=mpf(3.990996828344735e-08)
	total+=mpf(2.4198036634689936e-19)
	total+=mpf(2.346340935893772e-95)
	total+=mpf(1.6741688035677474e-07)
	print(total)


if __name__== "__main__":
  main()