import pytxchart as m

crt = m.PyTxChart()
crt.read(r"A3934.CRT")
crt_data = crt.get_data()
assert crt_data['desc']['Chart_name'] == '3935'
assert crt_data['desc']['File_name'] == 'A3934'
assert crt_data['desc']['Date_corr'] == '07-02-2002'