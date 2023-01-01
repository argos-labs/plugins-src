username = 'irene@argos-labs.com'
password = '..'
security_token = '..'
#self.dict_dt = self.sf.query("select id from ")['records']

# 0JZ5w000000jLElGAM, Second call
# 0JZ5w000000j7tQGAQ, pwd
import js2py
f = js2py.eval_js("function openInWidget(id) {sforce.console.selectMacro()}")
print(f('0JZ5w000000jLElGAM'))