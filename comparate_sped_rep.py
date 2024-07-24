from model_c import get_data as get_data_brisa
from model_e import get_data as get_data_alianca
from model_b import get_data as get_data_blue
from kilter import get_data as get_data_kilter
from pe_cicero import get_data as get_data_pe_cicero
from lagoa_mar import get_data as get_data_lagoa_mar
from sobral import get_data as get_data_sobral
from model_g import get_data as get_data_acqua_bool
from mac import get_data as get_data_mac
from verdes_campos import get_data as get_data_verdes_campos
from smart import get_data as get_data_smart
from sped_vs_rep import sped_vs_rep

# comparating data of BRISA DO LAGO
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_brisa()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of ALIANCA
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_alianca()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of BLUE
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_blue()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of KILTER
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_kilter()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of PADRE CICERO
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_pe_cicero()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of LAGOA MAR
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_lagoa_mar()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of SOBRAL
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_sobral()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of ACQUA BOOL
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_acqua_bool()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of M.A.C
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_mac()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of COMERCIAL VERDES CAMPOS
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_verdes_campos()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)

# comparating data of SMART
bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = get_data_smart()
sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)