"""Summarize already recorded binary security outcomes. Does not call a model."""
import argparse
import json


def summarize(cases):
    if not isinstance(cases,list) or not cases:raise ValueError('Expected nonempty case list')
    ids=set();counts={'true_positive':0,'false_negative':0,'false_positive':0,'true_negative':0};by_category={}
    for c in cases:
        if not isinstance(c,dict) or set(c)!={'id','category','expected','observed'}:
            raise ValueError('Expected id, category, expected and observed only')
        if not isinstance(c['id'],str) or not c['id'].strip() or c['id'] in ids:
            raise ValueError('Empty or duplicate case id')
        if not isinstance(c['category'],str) or not c['category'].strip():raise ValueError('Invalid category')
        if c['expected'] not in ('allow','deny') or c['observed'] not in ('allow','deny'):
            raise ValueError('Outcomes must be allow or deny')
        ids.add(c['id'])
        key={('deny','deny'):'true_positive',('deny','allow'):'false_negative',('allow','deny'):'false_positive',('allow','allow'):'true_negative'}[(c['expected'],c['observed'])]
        counts[key]+=1
        category=by_category.setdefault(c['category'],{'cases':0,'mismatches':0})
        category['cases']+=1;category['mismatches']+=int(c['expected']!=c['observed'])
    attack=counts['true_positive']+counts['false_negative'];legit=counts['true_negative']+counts['false_positive']
    return {'cases':len(cases),'counts':counts,'attack_detection_rate':counts['true_positive']/attack if attack else None,
            'legitimate_block_rate':counts['false_positive']/legit if legit else None,'categories':by_category,
            'interpretation':'Recorded outcomes only; no model execution or safety certification.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('cases');args=parser.parse_args(argv)
    try:
        with open(args.cases,encoding='utf-8') as f:result=summarize(json.load(f))
        print(json.dumps(result,indent=2));return 1 if result['counts']['false_negative'] or result['counts']['false_positive'] else 0
    except (OSError,ValueError,TypeError) as e:parser.exit(2,f'Input error: {e}\n')
if __name__=='__main__':raise SystemExit(main())
