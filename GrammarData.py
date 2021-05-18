english_prepositions_dictionary = ['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'next', 'of', 'off', 'on', 'onto', 'opposite', 'out', 'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'till', 'to', 'toward', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without']

template_english_verb='''
{{ 
  "ENG" : {{
    "DEFINITION":"{}",
    "ENG" :"{}",
    "IS_REGULAR" : {},
    "IS_TRANSITIVE" : {},
    "PREPOSITIONS" : {}
    }},'''

template_german_verb='''
  "GER" : {{
    "AXULIAR_VERB" : "{}",
    "DEFINITION" : "{}",
    "GER" : "{}",
    "IS_REFLEXIBLE": {},
    "IS_SEPARABLE" : {},
    "PREPOSITIONS" : {}
}},'''

template_spanish_verb='''
    "SPA" : {{
      "DEFINITION" : "{}",
      "IS_REGULAR" : {},
      "SPA" : "{}"}}
}}'''

template_eng_adjective='''
{{
  "ENG": {{
    "DEFINITION":"{}",
    "ENG":"{}",
    "EXAMPLE":"None"}},'''

template_spa_adjective='''
  "SPA":{{
    "DEFINITION" : "{}",
    "SPA":"{}",
    "EXAMPLE":"None"}},
'''

template_ger_adjective='''
  "GER":{{
    "DEFINITION" : "{}",
    "GER":"{}",
    "EXAMPLE":"None"}},

}}'''