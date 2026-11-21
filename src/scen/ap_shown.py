# running states written as shown, in capitals: case doesn't matter (*Appliance run*, *Entities*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S]['state'] = 'program_running'; TRANSLATED[S] = 'Running'
INPUTS['running_states'] = ['RUNNING']
EXPECT = ['14:32', '62']
EXPECT_NOT = ['NOT RUNNING']
EXPECT_SHARE = 62
