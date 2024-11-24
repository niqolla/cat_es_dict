from django.shortcuts import render, redirect
from .forms import TurbiniForm

import os
from django.conf import settings
import pandas as pd

import re

turbini_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'app', 'resource', 'turbini.csv'))
katalog_df = pd.read_csv(os.path.join(settings.BASE_DIR, 'app', 'resource', 'katalog.csv'))

## pretraga trubine
def najdi_turbina_po_shifra(shifra):

    shifra_query_jrone = turbini_df[turbini_df['query_jrone_no'] == shifra]
    shifra_query_oe1 = turbini_df[turbini_df['query_oe1'] == shifra]
    shifra_query_oe2 = turbini_df[turbini_df['query_oe2'] == shifra]

    shifra_query = pd.concat([shifra_query_jrone, shifra_query_oe1, shifra_query_oe2])

    return shifra_query

## pretraga trubine
def get_results_for_turbine(passed_request):

    auto = passed_request.GET['auto']
    CCM = passed_request.GET['CCM']
    HP = passed_request.GET['HP']

    shifra = passed_request.GET['shifra'].replace('-','').upper()

    result_df = turbini_df

    if auto != '':
        auto_query_res = turbini_df[turbini_df['marka'] == auto]
        result_df = pd.merge(result_df, auto_query_res[['jrone_no', 'marka']], how='inner', on=['jrone_no', 'marka'])

    if CCM != '':
        CCM_query_res = turbini_df[turbini_df['ccm_numbers'] == CCM]
        result_df = pd.merge(result_df, CCM_query_res[['jrone_no', 'ccm_numbers']], how='inner', on=['jrone_no', 'ccm_numbers'])

    if HP != '':
        HP = int(HP)
        HP_query_res = turbini_df[turbini_df['snaga_numbers'] == HP]
        result_df = pd.merge(result_df, HP_query_res[['jrone_no', 'snaga_numbers']], how='inner', on=['jrone_no', 'snaga_numbers'])

    if shifra != '':
        shifra_query = najdi_turbina_po_shifra(shifra=shifra)
        result_df = pd.merge(result_df, shifra_query['jrone_no'], how='inner', on='jrone_no')

    result_df.drop_duplicates(inplace=True)

    result_to_return_grouped_by_jrone_no = []    

    for jrone_no in result_df.jrone_no.unique():
        result_to_return_grouped_by_jrone_no.append(result_df[result_df['jrone_no'] == jrone_no].values.tolist())
    
    return result_to_return_grouped_by_jrone_no


## pretraga trubine
def home(request):
    if not request.GET.keys() or (request.GET['auto'] == '' and request.GET['shifra'] == ''
                                  and request.GET['CCM'] == '' and request.GET['HP'] == ''):
        turbini_form = TurbiniForm

    else:
        result_to_return_grouped_by_jrone_no = get_results_for_turbine(passed_request=request)
        if len(result_to_return_grouped_by_jrone_no) == 0 :
            nema_rez = True
        else:
            nema_rez = False

        turbini_form = TurbiniForm(request.GET)
        
        context_dict = {'grouped_by_jrone_no_LoLoL' : result_to_return_grouped_by_jrone_no,
                        'turbini_form' : turbini_form,
                        'nema_rez':nema_rez
                        }
        
        return render(request, 'app/turbini.html', context_dict)

    return render(request, 'app/home.html', {'turbini_form':turbini_form})

def kontakt(request):
    return render(request, 'app/kontakt.html')

def informacije(request):
    return render(request, 'app/informacije.html')

## pretraga SVE
def pretraga(request):
    query = request.GET.get('query', '').upper()

    pretraga_return_cols = ['turbo_maker_oe_no', 'turbo_maker', 'turbo_model', 'vehicle_oem_number', 'vehicle_brand', 'vehicle_model', 'engine']

    if query == '':
        context_dict = {}
    
    elif re.compile(r'^\d{4}-\d{4}$').match(query):
        prefix, sufix = query.split('-')

        isti_rezultati = katalog_df[
                    (katalog_df['query_turbo_maker_oe_no'].str.startswith(prefix, na=False)) &
                    (katalog_df['query_turbo_maker_oe_no'].str.endswith(sufix, na=False))
                    ][pretraga_return_cols].fillna('/').values.tolist()
        
        context_dict = {
                'isti_rezultati' : isti_rezultati
                }
    else:
        query = query.replace(' ', '').replace('-', '')

        isti_rezultati = katalog_df[
                    katalog_df['query_turbo_maker_oe_no'].str.startswith(query, na=False)
                    ][pretraga_return_cols].fillna('/').values.tolist()
        
        context_dict = {
            'isti_rezultati' : isti_rezultati, 
            }

        if len(query) == 10:

            slicno_query = query[:-4]

            slicni_rezultati = katalog_df[
                    katalog_df['query_turbo_maker_oe_no'].str.startswith(slicno_query, na=False)
                    ][pretraga_return_cols].fillna('/').values.tolist()

            for rez in isti_rezultati:
                if rez in slicni_rezultati:
                    slicni_rezultati.remove(rez)
            
            context_dict['slicni_rezultati'] = slicni_rezultati

        elif len(query) == 8:
            prefix, sufix = query[:4], query[-4:]

            slicni_rezultati = katalog_df[
                        (katalog_df['query_turbo_maker_oe_no'].str.startswith(prefix, na=False)) &
                        (katalog_df['query_turbo_maker_oe_no'].str.endswith(sufix, na=False))
                        ][pretraga_return_cols].fillna('/').values.tolist()
            
            context_dict['slicni_rezultati'] = slicni_rezultati

    if 'slicni_rezultati' not in context_dict and 'isti_rezultati' not in context_dict:
        
        context_dict['nema_rezultati'] = True

    elif ('isti_rezultati' in context_dict and 
          len(context_dict['isti_rezultati']) == 0
          and ('slicni_rezultati' not in context_dict 
               or ('slicni_rezultati' in context_dict 
                   and len(context_dict['slicni_rezultati']) == 0
                   ) 
               )):

        context_dict['nema_rezultati'] = True
        
    elif  ('slicni_rezultati' in context_dict and 
          len(context_dict['slicni_rezultati']) == 0
          and ('isti_rezultati' not in context_dict 
               or ('isti_rezultati' in context_dict 
                   and len(context_dict['isti_rezultati']) == 0
                   ) 
               )):
        
        context_dict['nema_rezultati'] = True

    else:
        pass

    if 'nema_rezultati' in context_dict and context_dict['nema_rezultati'] == True:

        result_df = [najdi_turbina_po_shifra(shifra=query).values]

        if len(result_df[0]) != 0:
            context_dict = {'grouped_by_jrone_no_LoLoL' : result_df,}
            return render(request, 'app/turbini.html', context_dict)

    return render(request, 'app/pretraga.html', context=context_dict)

def ArtiklInfo(request, turbo_maker_oe_no):
    original_query = turbo_maker_oe_no.upper()
    turbo_maker_oe_no = turbo_maker_oe_no.replace(' ', '').replace('-', '').upper()

    artikl_return_cols = ['turbo_maker_oe_no', 
                            'turbo_maker',
                            'turbo_model',
                            'vehicle_oem_number',
                            'vehicle_brand',
                            'vehicle_model',
                            'engine',
                            'year',
                            'complete_turbo_code',
                            'gasket_kits',
                            'chra',
                            'sw',
                            'cw',
                            'back_plate',
                            'thrust_flinger',
                            'thrust_bearing',
                            'journal_bearing',
                            'bearing_housing',
                            'actuator',
                            'turbine_housing',
                            'compressor_housing',
                            'nozzle_ring_assembly',
                            'repair_kits',
                            ]

    isti_rezultati = katalog_df[
                    katalog_df['query_turbo_maker_oe_no'] == str(turbo_maker_oe_no)
                    ][artikl_return_cols].fillna('/').values.tolist()
    
    context_dict = {
        'isti_rezultati' : isti_rezultati ,
        'original_query': original_query}

    return render(request, 'app/artikl.html', context=context_dict)


def kako_funkcionise_turbo(request):
    return render(request, 'app/informacije/kako-funkcionise-turbo.html')

def simptomi_kvara_turbine(request):
    return render(request, 'app/informacije/simptomi-kvara-turbine.html')

def zasto_se_kvari_turbina(request):
    return render(request, 'app/informacije/zasto-se-kvari-turbina.html')

def zasto_turbina_trosi_ulje(request):
    return render(request, 'app/informacije/zasto-turbina-trosi-ulje.html')

def instrukcije_za_montazu(request):
    return render(request, 'app/informacije/instrukcije-za-montazu.html')

