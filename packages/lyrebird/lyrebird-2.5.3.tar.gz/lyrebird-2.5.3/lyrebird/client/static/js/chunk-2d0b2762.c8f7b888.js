(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0b2762"],{"23e0":function(e,t,n){"use strict";n.r(t),n.d(t,"conf",function(){return o}),n.d(t,"language",function(){return a});var o={comments:{lineComment:"//"},brackets:[["{","}"],["[","]"],["(",")"]],autoClosingPairs:[{open:'"',close:'"',notIn:["string","comment"]},{open:"'",close:"'",notIn:["string","comment"]},{open:"{",close:"}",notIn:["string","comment"]},{open:"[",close:"]",notIn:["string","comment"]},{open:"(",close:")",notIn:["string","comment"]}],folding:{offSide:!0}},a={defaultToken:"",tokenPostfix:".pug",ignoreCase:!0,brackets:[{token:"delimiter.curly",open:"{",close:"}"},{token:"delimiter.array",open:"[",close:"]"},{token:"delimiter.parenthesis",open:"(",close:")"}],keywords:["append","block","case","default","doctype","each","else","extends","for","if","in","include","mixin","typeof","unless","var","when"],tags:["a","abbr","acronym","address","area","article","aside","audio","b","base","basefont","bdi","bdo","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","command","datalist","dd","del","details","dfn","div","dl","dt","em","embed","fieldset","figcaption","figure","font","footer","form","frame","frameset","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","iframe","img","input","ins","keygen","kbd","label","li","link","map","mark","menu","meta","meter","nav","noframes","noscript","object","ol","optgroup","option","output","p","param","pre","progress","q","rp","rt","ruby","s","samp","script","section","select","small","source","span","strike","strong","style","sub","summary","sup","table","tbody","td","textarea","tfoot","th","thead","time","title","tr","tracks","tt","u","ul","video","wbr"],symbols:/[\+\-\*\%\&\|\!\=\/\.\,\:]+/,escapes:/\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,tokenizer:{root:[[/^(\s*)([a-zA-Z_-][\w-]*)/,{cases:{"$2@tags":{cases:{"@eos":["","tag"],"@default":["",{token:"tag",next:"@tag.$1"}]}},"$2@keywords":["",{token:"keyword.$2"}],"@default":["",""]}}],[/^(\s*)(#[a-zA-Z_-][\w-]*)/,{cases:{"@eos":["","tag.id"],"@default":["",{token:"tag.id",next:"@tag.$1"}]}}],[/^(\s*)(\.[a-zA-Z_-][\w-]*)/,{cases:{"@eos":["","tag.class"],"@default":["",{token:"tag.class",next:"@tag.$1"}]}}],[/^(\s*)(\|.*)$/,""],{include:"@whitespace"},[/[a-zA-Z_$][\w$]*/,{cases:{"@keywords":{token:"keyword.$0"},"@default":""}}],[/[{}()\[\]]/,"@brackets"],[/@symbols/,"delimiter"],[/\d+\.\d+([eE][\-+]?\d+)?/,"number.float"],[/\d+/,"number"],[/"/,"string",'@string."'],[/'/,"string","@string.'"]],tag:[[/(\.)(\s*$)/,[{token:"delimiter",next:"@blockText.$S2."},""]],[/\s+/,{token:"",next:"@simpleText"}],[/#[a-zA-Z_-][\w-]*/,{cases:{"@eos":{token:"tag.id",next:"@pop"},"@default":"tag.id"}}],[/\.[a-zA-Z_-][\w-]*/,{cases:{"@eos":{token:"tag.class",next:"@pop"},"@default":"tag.class"}}],[/\(/,{token:"delimiter.parenthesis",next:"@attributeList"}]],simpleText:[[/[^#]+$/,{token:"",next:"@popall"}],[/[^#]+/,{token:""}],[/(#{)([^}]*)(})/,{cases:{"@eos":["interpolation.delimiter","interpolation",{token:"interpolation.delimiter",next:"@popall"}],"@default":["interpolation.delimiter","interpolation","interpolation.delimiter"]}}],[/#$/,{token:"",next:"@popall"}],[/#/,""]],attributeList:[[/\s+/,""],[/(\w+)(\s*=\s*)("|')/,["attribute.name","delimiter",{token:"attribute.value",next:"@value.$3"}]],[/\w+/,"attribute.name"],[/,/,{cases:{"@eos":{token:"attribute.delimiter",next:"@popall"},"@default":"attribute.delimiter"}}],[/\)$/,{token:"delimiter.parenthesis",next:"@popall"}],[/\)/,{token:"delimiter.parenthesis",next:"@pop"}]],whitespace:[[/^(\s*)(\/\/.*)$/,{token:"comment",next:"@blockText.$1.comment"}],[/[ \t\r\n]+/,""],[/<!--/,{token:"comment",next:"@comment"}]],blockText:[[/^\s+.*$/,{cases:{"($S2\\s+.*$)":{token:"$S3"},"@default":{token:"@rematch",next:"@popall"}}}],[/./,{token:"@rematch",next:"@popall"}]],comment:[[/[^<\-]+/,"comment.content"],[/-->/,{token:"comment",next:"@pop"}],[/<!--/,"comment.content.invalid"],[/[<\-]/,"comment.content"]],string:[[/[^\\"'#]+/,{cases:{"@eos":{token:"string",next:"@popall"},"@default":"string"}}],[/@escapes/,{cases:{"@eos":{token:"string.escape",next:"@popall"},"@default":"string.escape"}}],[/\\./,{cases:{"@eos":{token:"string.escape.invalid",next:"@popall"},"@default":"string.escape.invalid"}}],[/(#{)([^}]*)(})/,["interpolation.delimiter","interpolation","interpolation.delimiter"]],[/#/,"string"],[/["']/,{cases:{"$#==$S2":{token:"string",next:"@pop"},"@default":{token:"string"}}}]],value:[[/[^\\"']+/,{cases:{"@eos":{token:"attribute.value",next:"@popall"},"@default":"attribute.value"}}],[/\\./,{cases:{"@eos":{token:"attribute.value",next:"@popall"},"@default":"attribute.value"}}],[/["']/,{cases:{"$#==$S2":{token:"attribute.value",next:"@pop"},"@default":{token:"attribute.value"}}}]]}}}}]);