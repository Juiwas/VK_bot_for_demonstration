from Scenarios.unified_manual import check_script_unified_manual
from Scenarios.kogda_viplata import check_script_kogda_viplata
from Scenarios.kakie_dokument import check_script_kakie_dokument
from Scenarios.odobrenie import check_script_odobrenie
from Scenarios.no_mera import check_script_no_mera
from Scenarios.prodlenie import check_script_prodlenie
from Scenarios.chto_poligeno import check_script_chto_poligeno
from Scenarios.no_filial import check_script_no_filial
from Scenarios.filiаl import check_script_filifl
from Scenarios.thank import check_script_thank



check_scenarios = {"Телефон/госуслуги": check_script_odobrenie,
					"Какие документы": check_script_kakie_dokument,
					"Когда выплата":check_script_kogda_viplata,
					"Узнать меру":check_script_no_mera,
					"Продление": check_script_prodlenie,
					"Опрос":check_script_chto_poligeno,
					"Узнать филиал":check_script_no_filial,
					"Филиал": check_script_filifl,
					"Благодарность": check_script_thank}




