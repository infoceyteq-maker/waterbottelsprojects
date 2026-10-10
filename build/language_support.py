"""Shared language selector helpers for generated static pages.

The source pack is mixed-language: explicit `.si`/`.en` pairs are switched,
while text with no translation stays visible as a fallback instead of
vanishing. The selected language is shared by all generated pages.
"""
import re


_PAIR_TEXT = re.compile(
    r">([^<>]*?[\u0D80-\u0DFF][^<>]*?)\s*/\s*([^<>]*?[A-Za-z][^<>]*?)<"
)


def mark_bilingual_pairs(document):
    """Wrap plain-text ``Sinhala / English`` pairs for the language switcher."""
    def replace(match):
        left, right = match.group(1).rstrip(), match.group(2).lstrip()
        if not re.search(r"[\u0D80-\u0DFF]", left) or not re.search(r"[A-Za-z]", right):
            return match.group(0)
        return (f'><span class="si">{left}</span>'
                f'<span class="en">{right}</span><')
    return _PAIR_TEXT.sub(replace, document)


_EMPTY_TD = re.compile(r'(<td\b[^>]*>)\s*</td>', re.I)
_TEXT_NODE = re.compile(r'>([^<>]+)<')
_PROMPT_TOKEN = re.compile(r'\[[^\]\n]*\]|_{3,}')
_CONFIRMATION = re.compile(
    r'(?<![\w])(?:to confirm|needs confirmation|verify|'
    r'තහවුරු කළ යුතුයි|තහවුරු කළ යුතු|තහවුරු කරන්න|තහවුරු කරගන්න)(?![\w])',
    re.I,
)
_PROMPT_WORDS = re.compile(r'_{2,}|\b(?:enter|to be completed|to confirm|tbc|select|choose|fill in|to agree|agree|to set|set|to calculate|calculate)\b', re.I)
_TD = re.compile(r'(<td\b[^>]*>)(.*?)(</td>)', re.I | re.S)
_PRIORITY_WORD = re.compile(r'(?<![A-Za-z0-9_-])(Critical|Mandatory|High)(?![A-Za-z0-9_-])')


def fill_empty_table_cells(document, marker='—'):
    """Make N/A financial/document cells explicit without inventing values."""
    return _EMPTY_TD.sub(lambda match: f'{match.group(1)}{marker}</td>', document)


def highlight_prompts(document):
    """Highlight fill-in prompts and verification language in rendered HTML."""
    def decorate_text(match):
        text = match.group(1)
        def prompt(match_token):
            token = match_token.group(0)
            if not _PROMPT_WORDS.search(token):
                return token
            return f'<mark class="to-complete">{token}</mark>'
        text = _PROMPT_TOKEN.sub(prompt, text)
        pieces = re.split(r'(<mark\b[^>]*>.*?</mark>)', text, flags=re.S)
        for index, part in enumerate(pieces):
            if not part.startswith('<mark'):
                pieces[index] = _CONFIRMATION.sub(
                    lambda m: f'<mark class="to-confirm">{m.group(0)}</mark>', part)
        return '>' + ''.join(pieces) + '<'
    return _TEXT_NODE.sub(decorate_text, document)


def highlight_table_priorities(document):
    """Show checklist priorities as colored badges in document tables."""
    classes = {"Critical": "priority-critical", "Mandatory": "priority-mandatory",
               "High": "priority-high"}
    def decorate_cell(match):
        def badge(word):
            value = word.group(0)
            return f'<span class="priority-tag {classes[value]}">{value}</span>'
        content = _PRIORITY_WORD.sub(badge, match.group(2))
        return match.group(1) + content + match.group(3)
    return _TD.sub(decorate_cell, document)


LANGUAGE_SWITCH = '''<label class="language-switch">
  <span class="language-switch-label"><span class="si">භාෂාව</span><span class="en">Language</span></span>
  <select class="language-select" aria-label="Select language">
    <option value="si">සිංහල</option>
    <option value="en">English</option>
  </select>
</label>'''

# Google Fonts for every generated page: Inter for Latin text and Noto Sans
# Sinhala for the Sinhala script. Loaded here because LANGUAGE_BOOTSTRAP is
# injected into the <head> of every page the build writes.
FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Sinhala:wght@400;500;600;700;800&display=swap">'''

LANGUAGE_BOOTSTRAP = FONT_LINKS + r'''
<script>
(function(){
  var lang='si';
  try { var saved=localStorage.getItem('wb-project-language');
    if(saved==='si'||saved==='en') lang=saved;
  } catch(e) {}
  document.documentElement.lang=lang;
  document.documentElement.setAttribute('data-language',lang);
})();
</script>'''

LANGUAGE_JS = r'''(function(){
  var KEY='wb-project-language';
  var SINHALA=/[\u0D80-\u0DFF]/;
  var BLOCK_TAGS=/^(P|H[1-6]|LI|TD|TH|BUTTON|A|LABEL|SUMMARY)$/;
  var LANGUAGE_RUNS=/[\u0D80-\u0DFF]+|[^\u0D80-\u0DFF]+/g;

  function nearestBlock(el){
    var node=el.parentElement;
    while(node && node!==document.body){
      if(BLOCK_TAGS.test(node.tagName) || node.classList.contains('pc-desc') ||
         node.classList.contains('hsub') || node.classList.contains('brand')) return node;
      node=node.parentElement;
    }
    return el.parentElement || document.body;
  }

  function annotatePairedBlocks(){
    var blocks=new Set();
    document.querySelectorAll('.en').forEach(function(el){blocks.add(nearestBlock(el));});
    blocks.forEach(function(block){
      if(!block) return;
      function wrapRuns(node){
        Array.prototype.slice.call(node.childNodes).forEach(function(child){
          if(child.nodeType===Node.TEXT_NODE && SINHALA.test(child.nodeValue||'')){
            var parts=(child.nodeValue||'').match(LANGUAGE_RUNS)||[];
            var fragment=document.createDocumentFragment();
            parts.forEach(function(part){
              if(SINHALA.test(part)){
                var span=document.createElement('span');
                span.className='si'; span.textContent=part; fragment.appendChild(span);
              }else{
                fragment.appendChild(document.createTextNode(part));
              }
            });
            child.parentNode.replaceChild(fragment,child);
          }else if(child.nodeType===Node.ELEMENT_NODE &&
                   !child.matches('script,style,.en,.si,.nav-si')){
            wrapRuns(child);
          }
        });
      }
      wrapRuns(block);
    });
  }

  function hasSinhalaOutsideEnglish(el){
    var block=nearestBlock(el);
    if(!block) return false;
    var copy=block.cloneNode(true);
    copy.querySelectorAll('.en').forEach(function(n){n.remove();});
    return SINHALA.test(copy.textContent || '');
  }

  function hasEnglishCounterpart(el){
    var block=nearestBlock(el);
    if(!block) return false;
    return Array.prototype.some.call(block.querySelectorAll('.en'),function(n){
      return n!==el && !el.contains(n);
    });
  }

  function applyLanguage(lang, persist){
    if(lang!=='si' && lang!=='en') lang='si';
    document.documentElement.lang=lang;
    document.documentElement.setAttribute('data-language',lang);

    document.querySelectorAll('.en').forEach(function(el){
      // If the source has no Sinhala counterpart, keep the English wording as
      // the fallback even in Sinhala mode.
      el.hidden=(lang==='si' && hasSinhalaOutsideEnglish(el));
    });
    document.querySelectorAll('.si,.nav-si').forEach(function(el){
      // If the source has no English counterpart, keep Sinhala as the fallback.
      el.hidden=(lang==='en' && hasEnglishCounterpart(el));
    });
    document.querySelectorAll('.language-select').forEach(function(select){
      select.value=lang;
    });
    if(persist){
      try { localStorage.setItem(KEY,lang); } catch(e) {}
    }
    document.dispatchEvent(new CustomEvent('wb-language-change',{detail:{language:lang}}));
  }

  document.addEventListener('change',function(event){
    if(event.target && event.target.matches('.language-select'))
      applyLanguage(event.target.value,true);
  });

  var saved='si';
  try { var stored=localStorage.getItem(KEY); if(stored==='si'||stored==='en') saved=stored; } catch(e) {}
  function initializeLanguage(){annotatePairedBlocks();applyLanguage(saved,false);}
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',initializeLanguage);
  }else{
    initializeLanguage();
  }
})();'''
