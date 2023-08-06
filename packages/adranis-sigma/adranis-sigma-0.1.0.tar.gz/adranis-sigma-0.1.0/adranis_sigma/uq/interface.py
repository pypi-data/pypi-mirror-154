"""
Interface functions for Sigma-UQ. They are trying to replicate
the commands of type uq_xxx in UQLab.
"""
import numpy as np
import adranis_sigma.uq.helpers as helpers



class uq():
    """The UQ interface class
    """

    def __init__(self, session):
        self.session = session

    def createModule(self, of_type, Opts, nargout=1):
        """Generic method for creating a UQ Object aka
        UQ module in UQLab's terminology.

        Args:
            of_type (string): The type of object to create
            Opts (dict): The creation options
            nargout (int, optional): number of output arguments
                that are expected from the equivalent uq_createX
                command that will be executed in the UQLab worker
                on the cloud. Defaults to 1.

        Returns:
           dict: A dictionary of the UQ Object that was created
        """
        REQ = {
            'Command': f"uq_create{of_type.lower().title()}",
            'Argument': [{
                'Value': Opts
            }],
            'nargout': nargout,
        }
        resp = self.session.rest_call(request=REQ)
        return self.session.get_resp_value(resp)
        # return True

    def createInput(self, InputOpts):
        self.session.logger.debug("Starting the processing of Input options.")
        if "Marginals" in InputOpts:
            for idx, marginal in enumerate(InputOpts["Marginals"]):
                PARAMS_SPECIFIED = "Parameters" in marginal and marginal[
                    "Parameters"]
                MOMENTS_SPECIFIED = "Moments" in marginal and marginal[
                    "Moments"]
                self.session.logger.debug(
                    f"Marginal nr. {idx}: Parameters specified: {PARAMS_SPECIFIED}, "
                        "Moments specified: {MOMENTS_SPECIFIED}")
                # Address the issue of mixed Moments-Parameters specification:
                # The fix here is to give the non-specified one as empty list
                if PARAMS_SPECIFIED and MOMENTS_SPECIFIED:
                    msg = "Cannot have both parameters and moments specified for a Marginal!"
                    raise RuntimeError(msg)
                if PARAMS_SPECIFIED:
                    # make sure that Parameters are like this: [[a,b]] and not
                    # like this: [a,b]
                    if not isinstance(marginal["Parameters"][0], list):
                        marginal["Parameters"] = [marginal["Parameters"]]
                    marginal["Moments"] = []
                if MOMENTS_SPECIFIED:
                    # make sure that Moments are like this: [[a,b]] and not
                    # like this: [a,b]
                    if not isinstance(marginal["Moments"][0], list):
                        marginal["Moments"] = [marginal["Moments"]]
                    marginal["Parameters"] = []
        return self.createModule('input', InputOpts)

    def createModel(self, ModelOpts):
        # check the type of model:
        # Model: exists locally UNLESS it is an mString
        # MetaModel: exists remotely
        if ModelOpts['Type'].lower() in ['uq_default_model', 'model'
                                         ] and 'mString' not in ModelOpts:
            # assign a compatible value to Type
            ModelOpts['Type'] = 'uq_default_model'
            # local definition
            ModelOpts['mFile'] = 'uq_cloud_remote'
            # In this case the 'ModelFun' needs to be supplied to carry out
            # model evaluations
            assert 'ModelFun' in ModelOpts, 'The ModelFun field is required and has not been supplied!'
            if 'Parameters' in ModelOpts:
                ModelOpts['Parameters']['theModel'] = ModelOpts['ModelFun']
            else:
                ModelOpts['Parameters'] = {'theModel': ModelOpts['ModelFun']}
            return self.createModule('model', ModelOpts)
        else:
            if ModelOpts['Type'].lower() in ['uq_default_model', 'model']:
                ModelOpts['Type'] = 'uq_default_model'
            # remote definition
            return self.createModule('model', ModelOpts)

    def createAnalysis(self, AnalOpts):
        return self.createModule('analysis', AnalOpts)

    def getSample(self, Input=None, N=None, Method='MC', nargout=1):

        REQ = {'Command': 'uq_getSample', 'nargout': nargout}
        if Input is None:
            REQ['Argument'] = [{'Value': N}, {'Value': Method}]
        else:
            if isinstance(Input, str):
                REQ['Argument'] = [{
                    'Value': Input
                }, {
                    'Value': N
                }, {
                    'Value': Method
                }]
            elif isinstance(Input, dict):
                REQ['Argument'] = [{
                    'Value': Input['Name']
                }, {
                    'Value': N
                }, {
                    'Value': Method
                }]
            else:
                raise ValueError(f"Unsupported type of Input: {str(type(Input))}!")
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)

        if nargout <= 1:
            theSamples = np.array(resp_value, ndmin=2)
            # In case theSamples is a row vector we have to make a consistency check:
            # Is this correct (i.e. M>1 and N=1) or should it be transposed? (M=1 N>1)
            # For this we need some info from Input
            if theSamples.shape[0] == 1 and nargout == 1:
                if Input is None:
                    # in this case we really need the input so we have to make one more call
                    # to sigma
                    Input = self.getInput('')

                if isinstance(Input['Marginals'], dict):
                    M = 1
                else:
                    M = sum(
                        isinstance(x.get('Type'), str) for x in Input['Marginals'])
                if M == 1:
                    return theSamples.T
                else:
                    return theSamples
            else:
                return theSamples
        else:
            for idx, respi in enumerate(resp_value):
                respi = np.array(respi, ndmin=2)
                if N > 1 and respi.shape[0] == 1:
                    resp_value[idx] = respi.T
                else:
                    resp_value[idx] = respi
            return resp_value

    def evalModel(self, Model=None, X=None, nargout=1):
        if X is None:
            return None
        # make sure that X is correctly interpreted when a single sample is
        # provided
        X = np.array(X, ndmin=2)
        if Model is None:
            # If no Model is given get the currently selected one within the UQ
            # session
            Model = self.getModel('')
        # Check the type of model
        isLOCAL = Model['Type'].lower() in ['model', 'uq_default_model']
        isLOCAL = isLOCAL and 'mString' not in Model
        if not isLOCAL:
            REQ = {
                'Command':
                'uq_evalModel',
                'Argument': [{
                    'Value': Model['Name']
                }, {
                    'Value': helpers.jsonify_np_array(X)
                }],
                'nargout':
                nargout
            }

            # if we reached this far the model exists on the uq_worker
            resp = self.session.rest_call(request=REQ)
            resp_value = self.session.get_resp_value(resp)
        else:
            # Check whether there are parameters involved
            PARAMS_EXIST = len(Model['Parameters']) > 1
            # Is the model vectorized?
            IS_VECTORIZED = Model['isVectorized']
            # Assume that 'ModelFun' field exists, but make sure it is callable
            if PARAMS_EXIST and IS_VECTORIZED:
                resp_value = helpers.function_eval(Model['ModelFun'], X,
                                                   Model['Parameters'])
            elif PARAMS_EXIST and not IS_VECTORIZED:
                resp_value = []
                for x in X:
                    resp_value.append(
                        helpers.function_eval(Model['ModelFun'], x,
                                              Model['Parameters']))
                resp_value = np.array(resp_value)
            elif not PARAMS_EXIST and IS_VECTORIZED:
                resp_value = helpers.function_eval(Model['ModelFun'], X)
            else:  # not PARAMS_EXIST and not IS_VECTORIZED
                resp_value = []
                for x in X:
                    resp_value.append(
                        helpers.function_eval(Model['ModelFun'], x))
                resp_value = np.array(resp_value)

        # we have to make a consistency check
        if nargout > 1:
            for idx, respi in enumerate(resp_value):
                respi = np.array(respi, ndmin=2)
                if X.shape[0] > 1 and respi.shape[0] == 1:
                    resp_value[idx] = respi.T
                else:
                    resp_value[idx] = respi
        if nargout == 1:
            resp_value = np.array(resp_value, ndmin=2)
            if X.shape[0] > 1 and resp_value.shape[0] == 1:
                resp_value = resp_value.T
        return resp_value

    def getModule(self, of_type, name):
        if of_type == 'input':
            cmd = 'uq_getInput'
        if of_type == 'model':
            cmd = 'uq_getModel'
        if of_type == 'analysis':
            cmd = 'uq_getAnalysis'
        REQ = {'Command': cmd, 'Argument': [{'Value': name}]}
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def getInput(self, name):
        return self.getModule('input', name)

    def getModel(self, name):
        return self.getModule('model', name)

    def getAnalysis(self, name):
        return self.getModule('analysis', name)

    def getAnalysisResults(self, name):
        REQ = {
            'Command': 'uq_getAnalysisResults',
            'Argument': [{
                'Value': name
            }]
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def listModules(self, of_type):
        REQ = {
            'Command': 'uq_listModules',
            'Argument': [{
                'Value': of_type
            }],
            'nargout': 3
        }
        resp = self.session.rest_call(request=REQ)
        print(resp[2]['Value'])

    def listInputs(self):
        self.listModules('input')

    def listModels(self):
        self.listModules('model')

    def listAnalyses(self):
        self.listModules('analysis')

    def selectModule(self, of_type, name):
        if of_type == 'input':
            cmd = 'uq_selectInput'
        if of_type == 'model':
            cmd = 'uq_selectModel'
        if of_type == 'analysis':
            cmd = 'uq_selectAnalysis'

        REQ = {'Command': cmd, 'Argument': [{'Value': name}]}
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def selectInput(self, name):
        self.selectModule('input', name)

    def selectModel(self, name):
        self.selectModule('model', name)

    def selectAnalysis(self, name):
        self.selectModule('analysis', name)

    def removeModule(self, name, module_type):
        REQ = {
            'Command': 'uq_removeModule',
            'Argument': [{
                'Value': name
            }, {
                'Value': module_type.lower()
            }]
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def print(self, obj=None, name=None, of_type=None):
        if obj is None:
            moduleToPrint = {"Name": name, "Class": of_type}
        else:
            moduleToPrint = {"Name": obj["Name"], "Class": obj["Class"]}
        REQ = {'Command': 'uq_print', 'Argument': [{'Value': moduleToPrint}]}
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        print(resp_value)

    def display(self, obj=None, name=None, of_type=None, **kwargs):
        if obj is None:
            obj = self.getModule(of_type=of_type, name=name)
        return helpers.display(obj, self, **kwargs)

    def rng(self, seed=None, generator=None):
        if seed is None and generator is None:
            REQ = {
                'Command': 'uq_rng',
            }
        elif generator is None:
            # No generator specified but the seed is not None
            REQ = {'Command': 'uq_rng', 'Argument': [{'Value': seed}]}
        elif seed is None:
            # No seed specified but the generator is not None: return Error
            raise ValueError(
                'The seed value is required when specifying the generator.')
        else:
            # Both seed and generator specified
            REQ = {
                'Command': 'uq_rng',
                'Argument': [{
                    'Value': seed
                }, {
                    'Value': generator
                }]
            }
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def all_f(self, function=None, X=None, Marginals=None):
        if X is None or Marginals is None:
            return None
        REQ = {
            'Command':
            function,
            'Argument': [{
                'Value': helpers.jsonify_np_array(X)
            }, {
                'Value': Marginals
            }],
            'nargout':
            1
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = np.array(self.session.get_resp_value(resp), ndmin=2)
        return resp_value.reshape(X.shape)

    def all_cdf(self, X=None, Marginals=None):
        return self.all_f(function='uq_all_cdf', X=X, Marginals=Marginals)

    def all_pdf(self, X=None, Marginals=None):
        return self.all_f(function='uq_all_pdf', X=X, Marginals=Marginals)

    def all_invcdf(self, F=None, Marginals=None):
        return self.all_f(function='uq_all_invcdf', X=F, Marginals=Marginals)

    def GeneralIsopTransform(self, X, X_Marginals, X_Copula, Y_Marginals,
                             Y_Copula):
        REQ = {
            'Command':
            'uq_GeneralIsopTransform',
            'Argument': [{
                'Value': helpers.jsonify_np_array(X)
            }, {
                'Value': X_Marginals
            }, {
                'Value': X_Copula
            }, {
                'Value': Y_Marginals
            }, {
                'Value': Y_Copula
            }],
            'nargout':
            1
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = np.array(self.session.get_resp_value(resp), ndmin=2)
        return resp_value.reshape(X.shape)

    def extractObj(self, parentName, objPath, objType):
        REQ = {
            'Command':
            'uq_extractObj',
            'Argument': [{
                'Value': parentName
            }, {
                'Value': objPath
            }, {
                'Value': objType
            }],
            'nargout':
            1
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return resp_value

    def extractFromInput(self, parentName, objPath):
        return self.extractObj(parentName=parentName,
                               objPath=objPath,
                               objType="input")

    def extractFromModel(self, parentName, objPath):
        return self.extractObj(parentName=parentName,
                               objPath=objPath,
                               objType="model")

    def extractFromAnalysis(self, parentName, objPath):
        return self.extractObj(parentName=parentName,
                               objPath=objPath,
                               objType="analysis")

    def eval_Kernel(self, X1, X2, theta, Options):
        theta = np.asarray(theta)
        REQ = {
            'Command':
            'uq_eval_Kernel',
            'Argument': [{
                'Value': helpers.jsonify_np_array(X1)
            }, {
                'Value': helpers.jsonify_np_array(X2)
            }, {
                'Value': helpers.jsonify_np_array(theta)
            }, {
                'Value': Options
            }],
            'nargout':
            1
        }
        resp = self.session.rest_call(request=REQ)
        resp_value = self.session.get_resp_value(resp)
        return np.asarray(resp_value)

    # Input module, Copula-specific functions
    def PairCopula(self, family, theta, rotation=None):
        REQ = {
            'Command': 'uq_PairCopula',
            'Argument': [{
                'Value': family
            }, {
                'Value': theta
            }],
            'nargout': 1
        }
        if rotation is not None:
            REQ['Argument'].append({'Value': rotation})

        resp = self.session.rest_call(request=REQ)
        return self.session.get_resp_value(resp)

    def PairCopulaOperation(self, copula, operation, *args):
        REQ = {
            'Command': operation,
            'Argument': [{
                'Value': copula
            }],
            'nargout': 1
        }
        for arg in args:
            REQ["Argument"].append({'Value': arg})

        resp = self.session.rest_call(request=REQ)
        return self.session.get_resp_value(resp)

    def PairCopulaKendallTau(self, copula):
        """_summary_

        Args:
            copula (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.PairCopulaOperation(copula, 'uq_PairCopulaKendallTau')

    def PairCopulaUpperTailDep(self, copula):
        """_summary_

        Args:
            copula (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.PairCopulaOperation(copula, 'uq_PairCopulaUpperTailDep')

    def PairCopulaLowerTailDep(self, copula):
        """_summary_

        Args:
            copula (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.PairCopulaOperation(copula, 'uq_PairCopulaLowerTailDep')

    def CopulaSummary(self, copula, *args):
        """_summary_

        Args:
            copula (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.PairCopulaOperation(copula, 'uq_CopulaSummary', *args)

    def test_block_independence(self,
                                X,
                                alpha,
                                stat='Kendall',
                                correction='auto',
                                verbose=0,
                                nargout=1):
        """_summary_

        Args:
            X (_type_): _description_
            alpha (_type_): _description_
            stat (str, optional): _description_. Defaults to 'Kendall'.
            correction (str, optional): _description_. Defaults to 'auto'.
            verbose (int, optional): _description_. Defaults to 0.
            nargout (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        assert isinstance(
            X, list), "Requirement not satisfied: X should be a list!"
        REQ = {
            'Command':
            'uq_PairCopula',
            'Argument': [{
                'Value': X
            }, {
                'Value': alpha
            }, {
                'Value': stat
            }, {
                'Value': correction
            }, {
                'Value': verbose
            }],
            'nargout':
            nargout
        }
        resp = self.session.rest_call(request=REQ)
        return self.session.get_resp_value(resp)
