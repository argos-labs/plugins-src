"""
====================================
 :mod:`argoslabs.datanalysis.regression`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS data analysis using PANDAS basic
"""
# Authors
# ===========
#
# * Irene Cho
# * taehoon ahn
#
# Change Log
# --------
#  * [2024/07/01]
#    - plottype == 'CooksDistance' 기능 제거
#  * [2024/06/24]
#    - remove encoding option from to_excel()
#    - compare model 오류 수정
#    - plottype == 'CooksDistance' 오류 수정
#  * [2021/04/08]
#     - remove encoding option from read_excel()
#  * [2020/06/04]
#     - starting

################################################################################
import os
import sys
from io import StringIO

try:
    # noinspection PyUnresolvedReferences
    import tkinter as tk
except Exception:
    # sys.path.append(os.path.dirname(__file__))
    os.environ['MPLBACKEND'] = 'agg'
# noinspection PyUnresolvedReferences,PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
import pandas as pd
from sklearn import metrics, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, \
    LassoLars, OrthogonalMatchingPursuit, BayesianRidge, \
    PassiveAggressiveRegressor, \
    RANSACRegressor, TheilSenRegressor, HuberRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, \
    AdaBoostRegressor, GradientBoostingRegressor
from yellowbrick.regressor import ResidualsPlot, PredictionError, CooksDistance
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings

warnings.filterwarnings('ignore')


################################################################################
class Regression(object):
    # ==========================================================================
    model_lst = ['AdaBoost', 'BayesianRidge', 'DecisionTree', 'ElasticNet',
                 'ExtraTrees', 'GradientBoosting', 'Huber', 'KNeighbors',
                 'KernelRidge', 'Lasso', 'LassoLeastAngleRegression',
                 'LinearRegression', 'OrthogonalMatchingPursuit',
                 'PassiveAggressive', 'RandomForest',
                 'RandomSampleConsensus', 'Ridge', 'SupportVectorMachine',
                 'TheilSen']
    OP_TYPE = ['Fit Model', 'Compare Models']
    plottype = ['Residuals', 'PredictionError']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.model_type = argspec.modeltype
        self.test_size = argspec.test_size
        self.seed = argspec.seed
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.pred = None
        self.model = None

    # ==========================================================================
    def read_file(self):
        if not os.path.exists(self.argspec.datafile):
            raise IOError(f'Cannot read file "{self.argspec.datafile}"')
        _, ext = os.path.splitext(self.argspec.datafile)
        if ext.lower() in ('.xls', '.xlsx', '.xlsm'):
            self.df = pd.read_excel(self.argspec.datafile)
        elif ext.lower() in ('.csv', '.tsv'):
            self.df = pd.read_csv(self.argspec.datafile,
                                  encoding=self.argspec.encoding)
        elif ext.lower() in ('.json',):
            self.df = pd.read_json(self.argspec.datafile,
                                   encoding=self.argspec.encoding)
        else:
            raise ReferenceError(
                f'Not supported file extension "{ext}" for input. '
                f'One of ".xls", ".xlsx", ".csv", ".tsv", ".json"')

    # ==========================================================================
    def data_processing(self):
        self.y = self.df[self.argspec.y]
        self.df = self.df.drop(self.argspec.y, axis=1)
        if self.argspec.drop:
            self.X = self.df.drop(self.argspec.drop, axis=1)
        else:
            self.X = self.df
        if self.argspec.normalize == 'True':
            self.X = preprocessing.normalize(self.X)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, test_size=self.test_size,
                             random_state=self.seed)
        if self.argspec.onehotencoding == 'True':
            self.X_train = pd.get_dummies(self.X_train)
            self.X_test = pd.get_dummies(self.X_test)
        return self.X_train, self.X_test, self.y_train, self.y_test

    # ==========================================================================
    def set_model(self):
        if self.model_type == 'LinearRegression':
            self.model = LinearRegression()
        elif self.model_type == 'Lasso':
            self.model = Lasso(random_state=self.seed)
        elif self.model_type == 'Ridge':
            self.model = Ridge(random_state=self.seed)
        elif self.model_type == 'ElasticNet':
            self.model = ElasticNet(random_state=self.seed)
        elif self.model_type == 'LassoLeastAngleRegression':
            self.model = LassoLars()
        elif self.model_type == 'OrthogonalMatchingPursuit':
            self.model = OrthogonalMatchingPursuit()
        elif self.model_type == 'BayesianRidge':
            self.model = BayesianRidge()
        elif self.model_type == 'PassiveAggressive':
            self.model = PassiveAggressiveRegressor(random_state=self.seed)
        elif self.model_type == 'RandomSampleConsensus':
            self.model = RANSACRegressor(min_samples=0.5,
                                         random_state=self.seed)
        elif self.model_type == 'TheilSen':
            self.model = TheilSenRegressor(random_state=self.seed)
        elif self.model_type == 'Huber':
            self.model = HuberRegressor()
        elif self.model_type == 'KernelRidge':
            self.model = KernelRidge()
        elif self.model_type == 'SupportVectorMachine':
            self.model = SVR()
        elif self.model_type == 'KNeighbors':
            self.model = KNeighborsRegressor()
        elif self.model_type == 'DecisionTree':
            self.model = DecisionTreeRegressor(random_state=self.seed)
        elif self.model_type == 'RandomForest':
            self.model = RandomForestRegressor(random_state=self.seed)
        elif self.model_type == 'ExtraTrees':
            self.model = ExtraTreesRegressor(random_state=self.seed)
        elif self.model_type == 'AdaBoost':
            self.model = AdaBoostRegressor(random_state=self.seed)
        elif self.model_type == 'GradientBoosting':
            self.model = GradientBoostingRegressor(random_state=self.seed)
        self.model.fit(self.X_train, self.y_train)
        self.pred = self.model.predict(self.X_test)
        return self.y_test, self.pred

    # ==========================================================================
    def model_summary(self):
        mae = metrics.mean_absolute_error(self.y_test, self.pred)
        mse = metrics.mean_squared_error(self.y_test, self.pred)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(
            np.log(np.array(abs(self.pred)) + 1) - np.log(
                np.array(abs(self.y_test)) + 1),
            2)))
        r2 = metrics.r2_score(self.y_test, self.pred)
        mask = self.y_test != 0
        mape = (np.fabs(self.y_test - self.pred) / self.y_test)[mask].mean()
        accuracy = str(round((1 - mape) * 100, 2)) + '%'
        # results = pd.DataFrame(
        #     {'Model': self.model_type, 'MAE': [mae], 'MSE': [mse],
        #      'RMSE': [rmse], 'R2': [r2],
        #      'RMSLE': [rmsle], 'MAPE': [mape]}).round(3)
        # pth = os.path.join(os.path.dirname(self.argspec.datafile),
        #                    'model_summary.csv')
        # results.to_csv(pth)
        return mae.round(3), mse.round(3), rmse.round(3), rmsle.round(3), \
               round(r2, 3), mape.round(3), accuracy

    # ==========================================================================
    def printoutput(self):
        mae, mse, rmse, rmsle, r2, mape, accuracy = self.model_summary()
        with StringIO() as outst:
            lst = [['Model', 'MAE', 'MSE', 'RMSE', 'RMSLE', 'R2', 'MAPE',
                    'Accuracy'],
                   [self.model_type, round(mae, 3), round(mse, 3),
                    round(rmse, 3), round(rmsle, 3),
                    round(r2, 3), round(mape, 3), accuracy]]
            for i in range(len(lst)):
                for j in range(8):
                    outst.write(str(lst[i][j]))
                    outst.write(',')
                outst.write('\n')
            if self.argspec.plotoutput:
                self.plotting()
            print(outst.getvalue(), end='')

    # ==========================================================================
    def compare_models(self):
        mlst = [AdaBoostRegressor(random_state=self.seed), BayesianRidge(),
                DecisionTreeRegressor(random_state=self.seed),
                ElasticNet(random_state=self.seed),
                ExtraTreesRegressor(random_state=self.seed),
                GradientBoostingRegressor(random_state=self.seed),
                HuberRegressor(), KNeighborsRegressor(), KernelRidge(),
                Lasso(random_state=self.seed), LassoLars(),
                LinearRegression(), OrthogonalMatchingPursuit(),
                PassiveAggressiveRegressor(random_state=self.seed),
                RandomForestRegressor(random_state=self.seed),
                RANSACRegressor(min_samples=0.5, random_state=self.seed),
                Ridge(random_state=self.seed), SVR(),
                TheilSenRegressor(random_state=self.seed)]
        self.res = []
        for i in range(len(mlst)):
            model = mlst[i]
            model.fit(self.X_train, self.y_train)
            self.pred = model.predict(self.X_test)
            mae, mse, rmse, rmsle, r2, mape, accuracy = self.model_summary()
            self.res.append(
                {'Model': self.model_lst[i], 'MAE': mae, 'MSE': mse,
                 'RMSE': rmse, 'R2': r2,
                 'RMSLE': rmsle, 'MAPE': mape, 'Accuracy': accuracy})

        # result = pd.DataFrame(res).round(3).to_csv('compare.csv')
        def highlight_min(s):
            is_min = s == s.min()
            return ['background-color: yellow' if v else '' for v in is_min]

        def highlight_max(s):
            is_max = s == s.max()
            return ['background-color: yellow' if v else '' for v in is_max]

        self.res = pd.DataFrame(self.res).style.apply(highlight_min,
                                                      subset=['MAE', 'MSE',
                                                              'RMSE',
                                                              'RMSLE', 'MAPE'])
        self.res = self.res.apply(highlight_max, subset=['R2', 'Accuracy'])
        return self.res

    # ==========================================================================
    def plotting(self):
        visualizer = None
        if self.argspec.plottype == 'Residuals':
            visualizer = ResidualsPlot(self.model)
            visualizer.fit(self.X_train, self.y_train)
            visualizer.score(self.X_test, self.y_test)
        elif self.argspec.plottype == 'PredictionError':
            visualizer = PredictionError(self.model)
            visualizer.fit(self.X_train, self.y_train)
            visualizer.score(self.X_test, self.y_test)
        elif self.argspec.plottype == 'CooksDistance':
            visualizer = CooksDistance()
            x = np.array(self.X)
            y = np.array(self.y)
            visualizer.fit(x,y)
        # pltname = f'{self.argspec.plottype }.png'
        # pth  = os.path.join(os.path.dirname(self.argspec.datafile),pltname)
        visualizer.show(self.argspec.plotoutput)
        # print(os.path.abspath(self.argspec.plotoutput))

    # ==========================================================================
    def do(self, op):
        if op == 'Fit Model':
            self.set_model()
            self.printoutput()
        elif op == 'Compare Models':
            self.compare_models()
            pth = os.path.join(os.path.dirname(self.argspec.datafile),
                               'compare_models.html')
            html_str = self.res.highlight_max().to_string()
            with open(pth, 'w', encoding='utf-8') as f:
                f.write(html_str)
            print(os.path.abspath(pth), end='')
        else:
            raise RuntimeError('Invalid vision operation "%s"' % op)


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore")
        res = Regression(argspec)
        res.read_file()
        res.data_processing()
        res.do(argspec.op)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='4',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Regression',
            icon_path=get_icon_path(__file__),
            description='Data analysis using regression models',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('datafile', display_name='Dataset', help='dataset',
                          input_method='fileread')
        mcxt.add_argument('y', display_name='Target Variable', help='y value')
        mcxt.add_argument('op', display_name='Function type',
                          choices=Regression.OP_TYPE,
                          help='Regression type of operation')
        # ######################################## for app dependent options
        mcxt.add_argument('--drop', display_name='Drop Variables',
                          action='append',
                          help='drop values')
        mcxt.add_argument('--normalize', display_name='Normalization',
                          help='normalize the X_train', default='False')
        mcxt.add_argument('--onehotencoding', display_name='Onehot-Encoding',
                          help='get dummies for categorical variables',
                          default='False')
        mcxt.add_argument('--test_size', display_name='Testsize',
                          help='Size of test dataset', default=0.3, type=float)
        mcxt.add_argument('--seed', display_name='Seed', help='Set seed',
                          default=123, type=int)
        mcxt.add_argument('--modeltype', display_name='Model Type',
                          help='type of models', choices=Regression.model_lst)
        mcxt.add_argument('--plotoutput', display_name='Plot Output',
                          help='Absolute file path for output image',
                          input_method='fileread')
        mcxt.add_argument('--plottype', display_name='Plot Type',
                          help='type of plots', choices=Regression.plottype)
        mcxt.add_argument('--encoding',
                          display_name='Encoding',
                          default="utf-8",
                          help='Character encoding for input or output file, '
                               'default is [[utf-8]]')
        # mcxt.add_argument('--sheet-name',
        #                   display_name='Sheet Name',
        #                   default='0',
        #                   help='Choose sheet name or index (0-indexed) for '
        #                        'input. None for all sheets')

        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
