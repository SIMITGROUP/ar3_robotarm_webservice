class Routine:
    allowtypes = ['math','appendstring','call','callroutine','moveservo','movetrack','movejoint','movelinear','io','if']
    routinename=""
    content=""
    variables={}
    subroutines={}
    kern = None

    def __init__(self,kern):
        self.iswork = False
        self.kern = kern

    def load(self,routinename):
        filename = self.routinepath + "/" + routinename + self.routineextenstion
        if os.path.isfile(filename):
            try:
                f = open(filename)
                if f == False:
                    return "ERR_ROUTINE_NOTEXISTS"

                self.content = f.read()
                if is_json(self.content):
                    a=json.load(content)
                    self.routines=a['routines']
                    self.variables=a['variables']
                    self.iswork = True
                else:
                    self.iswork = False
                    self.routines = {}
                    self.variables = {}
                    return "ERR_ROUTINE_ISNOTJSON"
            except IOError:
                self.iswork = False
                self.routines = {}
                self.variables = {}
                return "ERR_ROUTINE_NOTEXISTS"
            finally:
                f.close()
            return ""

    def execute(self):
        result = self.executeSubRoutine('main')
    def executeSubRoutine(self,subroutinename):
        #validate subroutine exists
        if not subroutinename in self.subroutines.keys():
            return "ERR_ROUTINE_UNDEFINESUBROUTINE"
        srt = subroutines[subroutinename]
        arrlen = len(srt)
        for i in range(arrlen):
            attributes = srt[i]
            typename = attributes['type']

            if typename == None:
                return "ERR_UNDEFINED_SUBROUTINEUNDEFINETYPE"
            elif not typename in self.allowtypes:
                return "ERR_UNDEFINED_SUBROUTINEWRONGTYPE"
            else:
                actionname = 'run_'+typename
                if hasattr(self, actionname) and callable(getattr(self, actionname)):
                    res = getattr(self, actionname)(attributes)

        return "OK"


    # replace string with variable if it is defined in formula
    def applyVariable(self,val):
        #only replace variable if it is string
        if type(val) == str:
            for k,v in self.variables.items():
                val = val.replace(k,v)

        return val

    #apply mathematics formula into variables, it execute using eval and need careful with syntax no harmful
    def run_math(self,attr):
        # attr = { "type": "math",  "varname":"@runcount@","formula": " @runcount@ + 1" },
        varname = attr['varname']
        formula = attr['formula']
        if varname == None:
            return "ERR_SUBROUTINE_MATH_VARNAMEUNDEFINED"
        elif formula == None:
            return "ERR_SUBROUTINE_MATH_FORMULAUNDEFINED"

        formula = self.applyVariable(formula)
        #  = eval(formula)
        codeobj = compile(formula,'myformula','eval')

        if not codeobj:
            return "ERR_SUBROUTINE_FORMULASYNTAXERROR"
        else:
            self.variables[varname] = eval(formula)
            return "OK"

    #combine string
    def run_appendstring(self,attr):
        varname = attr['varname']
        formula = attr['formula']
        if varname == None:
            return "ERR_SUBROUTINE_MATH_VARNAMEUNDEFINED"
        elif formula == None:
            return "ERR_SUBROUTINE_MATH_FORMULAUNDEFINED"
        separator = ''
        self.variables[varname] = separator.join(formula)
        return "OK"

    # execute others subroutine
    def run_call(self,attr):
        # {"type": "call", "subroutines": ["opengripper1", "settrackhome"]},
        subroutines = attr['subroutines']

        if subroutines == None:
            return "ERR_SUBROUTINE_CALL_SUBROUTINEUNDEFINED"
        else:
            arrlen = len(subroutines)
            for i in range(arrlen):
                mysubroutine = subroutines[i]
                res = self.executeSubRoutine(mysubroutine)

                #error direct exit and return
                if self.isErrorCode(res):
                    return res
        return "OK"

    #execute external routine
    def run_callroutine(self,attr):
        # {"type": "callroutine", "routines": { "routine1":{ "@para1@": "my sample string from parent", "@j4home@": 20}}}
        for routinename, paras in  attr['routines'].items():
            rt = Routine(self.kern)
            success = rt.load(routinename)
            if not success:
                return "ERR_ROUTINE_INVALIDJSON"
            else:
                # pass variables into external routine
                for k, v in paras.items():
                    # map variable value if exists
                    v = self.applyVariable(v)
                    rt.variables[k] = v

                result = rt.execute()
                # if error, stop execution and return error msg
                if self.isErrorCode(result):
                    return result
        return "OK"


    def run_moveservo(self,attr):
        return self.applyMovement(attr)

    def run_movetrack(self,attr):
        return self.applyMovement(attr)

    def run_movejoint(self,attr):
        return self.applyMovement(attr)

    def run_movelinear(self,attr):
        return self.applyMovement(attr)

    def applyMovement(self,attr):
        if attr['type'] == None:
            return "ERR_UNDEFINED_SUBROUTINEUNDEFINETYPE"
        type = attr['type']
        movetype = attr['movetype']

        if movetype != None:
            if not movetype in ['absolute','move'] :
                return "ERR_SUBROUTINE_UNSUPPORTMOVETYPE"

        if type == 'movelinear':
            result = self.kern.moveLinear(attr['x'], attr['y'], attr['z'])

        elif type == 'movejoint':
            # move all joint in 1 go
            if movetype == 'absolute':
                result = self.kern.setPosition(attr['values'])
            # at this moment it can move joint by joint only
            elif movetype == 'move':
                for k,v in attr['values'].items():
                    result = self.kern.moveJoint(k, v, movetype)
                    #error, direct exit
                    if self.isErrorCode(result):
                        return result
        # move travel tracks, 1 at a time
        elif type == 'movetrack':
            for k, v in attr['values'].items():
                result = self.kern.moveTrack(trackname, mm, movetype)
                if self.isErrorCode(result):
                    return result

        # move servos, 1 at a time
        elif type == 'moveservo':
            for k, v in attr['values'].items():
                result = self.kern.moveServo(servoname, value)
                if self.isErrorCode(result):
                    return result
        return "OK"



    def isErrorCode(self,data):
        if type(data) == str and  self.left(data, 4) == 'ERR_':
            return True
        else:
            return False
