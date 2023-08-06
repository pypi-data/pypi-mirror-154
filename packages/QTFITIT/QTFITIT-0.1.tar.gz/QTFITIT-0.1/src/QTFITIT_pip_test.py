#Python standard library
import sys
#PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton,QSlider,QLabel,QLineEdit
#sklearn
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier,RandomForestRegressor
import joblib
#numpy matplotlib scipy
import numpy as np
import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import scipy
from scipy.interpolate import interp1d
#inport 3rd party library
import nlopt





# from fdmnes_conv import *

class myinput:
    def __init__(self,finp="input.txt"):
        input_dict = self.read_dict(finp)
        self.input_dict=input_dict
        self.file_energy = input_dict['file_energy']
        self.file_x = input_dict['file_x']
        self.file_y = input_dict['file_y']
        self.file_exp = input_dict['file_exp']
        self.fmodel = input_dict['fmodel']
        self.e1 = float(input_dict['e1'])
        self.e2 = float(input_dict['e2'])
        self.norm = float(input_dict['norm'])
        self.npar = int(input_dict['npar'])
        self.par_a = np.fromstring(input_dict['par_a'], dtype=float,sep=",")
        self.par_b = np.fromstring(input_dict['par_b'], dtype=float,sep=",")
        self.x0 = np.fromstring(input_dict['x0'], dtype=float,sep=",")
        self.par_name=input_dict['par_name'].split(',')
        ##########
        self.norm_a=(39/49)*self.norm
        self.norm_b=1.2*self.norm
        self.shift_a=-5
        self.shift_b=4.9
    # def init2(self):
    #     self.par_name = np.fromstring(input_dict['par_name'], dtype='U', sep=",")

    def read_dict(self,finp):
        input_dict = dict()
        with open(finp) as f:
            lines = f.readlines()
        for line in lines:
            tmp = line.split("$")
            input_dict[tmp[0]] = tmp[1]
        return input_dict

def ini_input():
    with open("input.txt") as f:
        tmp = f.readline()
        tmp = tmp.strip()
    input = myinput(tmp)
    return input
##########BEGIN TOOL BOX function
def obj_nl(x,other=None):
    res=obj(x)
    return res

def obj(x):
    input=ini_input()
    f = joblib.load(input.fmodel)
    energy = np.loadtxt(input.file_energy)
    exp = np.loadtxt(input.file_exp, skiprows=1)
    norm = input.norm
    # f = joblib.load("tmp.pkl")
    # energy = np.loadtxt("IHS_500_energy.txt")
    # exp = np.loadtxt("exp_excited.txt", skiprows=1)
    # norm = 33

    print(x)
    par=x.reshape([1,-1])
    mu = f.predict(par)
    mu = mu.reshape(mu.shape[1])
    mu = mu*norm

    fexp=interp1d(exp[:,0],exp[:,1],kind="cubic",fill_value='extrapolate')
    muexp=fexp(energy)
    res=np.linalg.norm(muexp-mu)
    return res


def obj_plot(x):
    input=ini_input()
    f = joblib.load(input.fmodel)
    energy = np.loadtxt(input.file_energy)
    exp = np.loadtxt(input.file_exp, skiprows=1)
    norm = input.norm
    e1 = input.e1
    e2 = input.e2
    # e1=7100
    # e2=7200


    print("AUTO FIT Structure Parameter: ",x)
    par=x.reshape([1,-1])
    mu = f.predict(par)
    mu = mu.reshape(mu.shape[1])
    mu = mu*norm

    fexp=interp1d(exp[:,0],exp[:,1],kind="cubic",fill_value='extrapolate')
    muexp=fexp(energy)
    res=np.linalg.norm(muexp-mu)
    #save
    out=np.vstack([energy,muexp,mu])
    np.savetxt("output_fitting_parameters",x)
    np.savetxt("output_fitting_spectra",out.T)
    #plot

    plt.close()
    plt.plot(energy,muexp,'b')
    plt.plot(energy,mu,'r')
    plt.legend(["experiment","calculation"])
    plt.xlim([e1,e2])
    plt.show()
    return res


def obj_old(x):
    print(x)
    norm = 33
    par=x.reshape([1,-1])
    f = joblib.load("IHS_500_ori.pkl")
    mu = f.predict(par)
    mu = mu.reshape(mu.shape[1])
    energy = np.loadtxt("IHS_500_energy.txt")
    Gamma_hole = 2.7;
    Ecent = 30;
    Elarg = 50;
    Gamma_max = 11;
    e0 = e0 = 7114.2;
    Efermi = 3 + e0;
    eip, muip = smooth_fdmnes(energy, mu, Gamma_hole, Ecent, Elarg, Gamma_max, Efermi)
    muip=muip*norm
    exp = np.loadtxt("exp_excited.txt", skiprows=1)
    fexp=interp1d(exp[:,0],exp[:,1],kind="cubic",fill_value='extrapolate')
    muexp=fexp(eip)
    res=np.linalg.norm(muexp-muip)
    return res
def obj_plot_old(x):
    print(x)
    norm = 33
    par=x.reshape([1,-1])
    f = joblib.load("IHS_500_ori.pkl")
    mu = f.predict(par)
    mu = mu.reshape(mu.shape[1])
    energy = np.loadtxt("IHS_500_energy.txt")
    Gamma_hole = 2.7;
    Ecent = 30;
    Elarg = 50;
    Gamma_max = 11;
    e0 = e0 = 7114.2;
    Efermi = 3 + e0;
    eip, muip = smooth_fdmnes(energy, mu, Gamma_hole, Ecent, Elarg, Gamma_max, Efermi)
    muip=muip*norm
    exp = np.loadtxt("exp_excited.txt", skiprows=1)
    fexp=interp1d(exp[:,0],exp[:,1],kind="cubic",fill_value='extrapolate')
    muexp=fexp(eip)
    res=np.linalg.norm(muexp-muip)

    plt.close()
    plt.plot(eip,muexp,'r')
    plt.plot(eip,muip,'b')
    plt.legend(["calculation", "experiment"])
    plt.xlim([7100, 7200])
    plt.show()
    return res
##########END TOOL BOX function



class QTFITIT(QWidget):


    def __init__(self):
        super().__init__()
        self.ini_input()
        self.setupUI()
        #invoke ini function

        self.ini_fitit()
        self.ini_model()
        return None

    def ini_input(self):
        with open("input.txt") as f:
            tmp = f.readline()
            tmp = tmp.strip()
        self.input = myinput(tmp)


    def ini_input3(self):
        self.fmodel = "tmp.pkl"  # current using
        #input file
        self.file_energy="Fephen3_Energy.txt"
        self.file_x="Fephen3_bond_3ligand.txt"
        self.file_y="Fephen3_xmu.txt"#convolution
        self.file_exp="exp_excited.txt"#exp spectrum

        # self.file_y = "IHS_500_spectra.txt"
        # self.fmodel="IHS_500_ori.pkl"#current using
        self.npar=3
        self.par_a=1.8*np.ones(self.npar)
        self.par_b=2.2*np.ones(self.npar)

        self.e1=7100
        self.e2=7200#plot energy range

        self.norm=1#change in model prediction
        ##########AUTO

        self.norm_a=(39/49)*self.norm
        self.norm_b=1.2*self.norm
        self.shift_a=-5
        self.shift_b=4.9
        return None

    def ini_input2(self):
        self.fmodel = "tmp.pkl"  # current using
        #input file
        self.file_energy="IHS_729_energy.txt"
        self.file_x="IHS_729_params.txt"
        self.file_y="IHS_729_mu_conv.txt"#convolution
        self.file_exp="exp_excited.txt"#exp spectrum

        # self.file_y = "IHS_500_spectra.txt"
        # self.fmodel="IHS_500_ori.pkl"#current using
        self.npar=6
        self.par_a=np.array([-0.3,-0.3,-0.3,-0.3,-0.3,-0.3])
        self.par_b=np.array([0.5,0.5,0.5,0.5,0.5,0.5])

        self.e1=7100
        self.e2=7200#plot energy range

        self.norm=32#change in model prediction
        ##########AUTO

        self.norm_a=(39/49)*self.norm
        self.norm_b=1.2*self.norm
        self.shift_a=-5
        self.shift_b=4.9
    def ini_input1(self):
        self.fmodel = "tmp.pkl"  # current using
        #input file
        self.file_energy="IHS_500_energy.txt"
        self.file_x="IHS_500_params.txt"
        self.file_y="IHS_500_mu_conv.txt"#convolution
        self.file_exp="exp_excited.txt"#exp spectrum

        # self.file_y = "IHS_500_spectra.txt"
        # self.fmodel="IHS_500_ori.pkl"#current using
        self.npar=3
        self.par_a=np.array([-0.3,-0.3,-0.3])
        self.par_b=np.array([0.5,0.5,0.5])

        self.e1=7100
        self.e2=7200#plot energy range

        self.norm=32#change in model prediction

        self.norm_a=(39/49)*self.norm
        self.norm_b=1.2*self.norm
        self.shift_a=-5
        self.shift_b=4.9




    def ini_fitit(self):
        # self.x = np.loadtxt(self.file_x)
        # self.y = np.loadtxt(self.file_y)
        # self.energy = np.loadtxt(self.file_energy)
        # self.exp = np.loadtxt(self.file_exp, skiprows=1)
        # self.par=np.zeros(self.npar)
        # #load model
        # self.f = joblib.load(self.fmodel)

        self.x = np.loadtxt(self.input.file_x)
        self.y = np.loadtxt(self.input.file_y)
        self.energy = np.loadtxt(self.input.file_energy)
        self.exp = np.loadtxt(self.input.file_exp, skiprows=1)
        self.par=np.zeros(self.input.npar)
        #load model
        # self.f = joblib.load(self.input.fmodel)




    def ini_label(self):
        # with open()
        # self.parname1
        return 0

    def ini_model(self):
        # x = np.loadtxt("IHS_500_params.txt", skiprows=1)
        # y = np.loadtxt("IHS_500_mu_conv.txt", skiprows=1)
        x = np.loadtxt(self.input.file_x)
        y = np.loadtxt(self.input.file_y)

        f = ExtraTreesRegressor()
        f.fit(x, y)
        joblib.dump(f, self.input.fmodel)
        self.f=f#using new fitted model

        print("Model OK")
        return 0

    def getpar(self):
        # par1=self.a1+float(self.slider1.value())/99*(self.b1-self.a1)
        # par2=self.a2+float(self.slider2.value())/99*(self.b2-self.a2)
        # par3 =self.a3 + float(self.slider3.value()) / 99 * (self.b3 - self.a3)
        # self.par=np.array([par1,par2,par3])

        par=[]
        for i in range(self.input.npar):
            slider=self.findChild(QtWidgets.QSlider, u'par' + str(i))
            tmp=self.input.par_a[i]+float( slider.value() )/99*( self.input.par_b[i]-self.input.par_a[i] )#QtWidgets.QSlider
            par.append(tmp)
        self.par=np.array(par)


        self.par=self.par.reshape([1,-1])#shape for skelarn prediction
        return 0
    def setpar(self,par):
        for i in range(self.input.npar):
            step=( self.input.par_b[i]-self.input.par_a[i] )/99
            val=(par[i]-self.input.par_a[i])/step
            val=np.ceil(val)
            slider = self.findChild(QtWidgets.QSlider, u'par' + str(i))
            slider.setValue(val)
        return None


    def getnorm(self):
        self.norm=self.input.norm_a + float(self.SliderNorm.value()) / 99 * (self.input.norm_b - self.input.norm_a)
        return 0

    def getshift(self):
        self.shift = self.input.shift_a + float(self.SliderShift.value()) / 99 * (self.input.shift_b - self.input.shift_a)
        return 0



    def cal(self):
        self.getpar()
        self.getnorm()
        self.getshift()
        par=self.par
        mu=self.f.predict(self.par)
        mu=mu.reshape(mu.shape[1])#reshape to array
        self.mu = mu * self.norm  # trans to object
        f=interp1d(self.energy+self.shift,self.mu,kind="cubic",fill_value="extrapolate")
        self.mu=f(self.energy)

        print("Norm is: ",self.norm)
        print("Energy Shift is: ",self.shift)
        print("Structure parameters is: ",par)
        plt.close()
        plt.plot(self.exp[:,0],self.exp[:,1],'b')
        plt.plot(self.energy,self.mu,'r')
        plt.legend(["experiment","calculation"])
        plt.xlim([self.input.e1,self.input.e2])
        plt.show()
    def save(self):
        fexp=interp1d(self.exp[:,0],self.exp[:,1],kind="cubic",fill_value="extrapolate")
        yexp=fexp(self.energy)
        out=np.vstack([self.energy,yexp,self.mu])
        np.savetxt("output_exp_reconstruction.txt",out.T)
        return None
    def fit(self):
        opt = nlopt.opt(nlopt.GN_DIRECT, self.input.npar)  # LN_COBYLA  LN_BOBYQA
        opt.set_lower_bounds(self.input.par_a)  # [-float('inf'), 0]
        opt.set_upper_bounds(self.input.par_b)
        opt.set_min_objective(obj_nl)
        opt.set_maxtime(30)#2 minuit
        # opt.set_maxeval(100)
        x = opt.optimize(self.input.x0)
        minf = opt.last_optimum_value()
        self.par=x
        obj_plot(x)#plot and save
        self.setpar(x)#set slider
        self.cal()#cal spectrum using new slider value

        print("Finish Auto Structure Fitting")
        print("Fitting Results is: ",x)
        return 0

    def fit_scipy(self):
        # x0 = np.array([0.2, 0.2, 0.2])
        x0=self.input.x0
        res = scipy.optimize.minimize(obj, x0, method='COBYLA', options={'maxiter': 20})
        obj_plot(res.x)
        print("Finish Auto Fitting")
        return res
    def fit_old(self):
        res=obj(self.par)
        print("obj: ",res)
        return res
    def print1(self):
        print(self.slider1.value())
    def setupUI(self):
        self.setWindowTitle("39Module_FITIT_of_PAPS-XAS-ML")
        grid = QGridLayout()
        grid.setSpacing(20)

        NSliderPar = 2
        for i in range(self.input.npar):
            # line = QLineEdit('par'+str(i))
            line = QLineEdit(self.input.par_name[i])
            grid.addWidget(line, (i+1) * 2-1, NSliderPar)

            slider = QSlider()
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setObjectName('par'+str(i))
            slider.sliderReleased.connect(self.cal)
            grid.addWidget(slider, (i+1) * 2, NSliderPar)

        ##########
        NSliderConv = 4
        NSliderConvLabel = NSliderConv

        self.LabelShift = QtWidgets.QLabel("Energy Shift")
        grid.addWidget(self.LabelShift, 1*2-1, NSliderConvLabel)
        self.SliderShift = QtWidgets.QSlider()
        self.SliderShift.setOrientation(QtCore.Qt.Horizontal)
        self.SliderShift.setValue(50)
        grid.addWidget(self.SliderShift, 1*2, NSliderConv)

        self.LabelNorm= QtWidgets.QLabel("Normalization Factor")
        grid.addWidget(self.LabelNorm, 2*2-1, NSliderConvLabel)
        self.SliderNorm = QtWidgets.QSlider()
        self.SliderNorm.setOrientation(QtCore.Qt.Horizontal)
        self.SliderNorm.setValue(50)
        grid.addWidget(self.SliderNorm, 2*2, NSliderConv)
        ##########
        self.pushButtonSave = QPushButton("SAVE")
        grid.addWidget(self.pushButtonSave, 1, 5)
        self.pushButtonFit = QPushButton("AUTO FIT Structure")
        grid.addWidget(self.pushButtonFit, 2, 5)
        self.pushButtonFitAll = QPushButton("AUTO FIT All")
        grid.addWidget(self.pushButtonFitAll, 3, 5)
        ##########
        self.setLayout(grid)
        ##########
        self.SliderNorm.sliderReleased.connect(self.cal)
        self.SliderShift.sliderReleased.connect(self.cal)
        ##########
        self.pushButtonFit.clicked.connect(self.fit)
        self.pushButtonSave.clicked.connect(self.save)

        return None
        # QtW

    def setupUI_old(self):
        self.setWindowTitle("39Module_FITIT_of_PAPS-XAS-ML")
        grid = QGridLayout()
        grid.setSpacing(20)

        # QtWidgets Defination
        NSliderPar = 2
        NSliderParLabel = NSliderPar

        self.label1 = QtWidgets.QLineEdit("par1")
        grid.addWidget(self.label1, 1 * 2 - 1, NSliderParLabel)

        self.label2 = QtWidgets.QLineEdit("par2")
        grid.addWidget(self.label2, 2 * 2 - 1, NSliderParLabel)

        self.label3 = QtWidgets.QLineEdit("par3")
        grid.addWidget(self.label3, 3 * 2 - 1, NSliderParLabel)

        self.label4 = QtWidgets.QLineEdit("par4")
        grid.addWidget(self.label4, 4 * 2 - 1, NSliderParLabel)

        self.label5 = QtWidgets.QLineEdit("par5")
        grid.addWidget(self.label5, 5 * 2 - 1, NSliderParLabel)

        self.label6 = QtWidgets.QLineEdit("par6")
        grid.addWidget(self.label6, 6 * 2 - 1, NSliderParLabel)

        self.label7 = QtWidgets.QLineEdit("par7")
        grid.addWidget(self.label7, 7 * 2 - 1, NSliderParLabel)

        self.label8 = QtWidgets.QLineEdit("par8")
        grid.addWidget(self.label8, 8 * 2 - 1, NSliderParLabel)

        self.label9 = QtWidgets.QLineEdit("par9")
        grid.addWidget(self.label9, 9 * 2 - 1, NSliderParLabel)

        self.label10 = QtWidgets.QLineEdit("par10")
        grid.addWidget(self.label10, 10 * 2 - 1, NSliderParLabel)

        # self.label = QtWidgets.QLineEdit("par")
        # grid.addWidget(self.label,  * 2 - 1, NSliderParLabel)

        self.slider1 = QtWidgets.QSlider()
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider1, 1 * 2, NSliderPar)

        self.slider2 = QtWidgets.QSlider()
        self.slider2.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider2, 2 * 2, NSliderPar)

        self.slider3 = QtWidgets.QSlider()
        self.slider3.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider3, 3 * 2, NSliderPar)

        self.slider4 = QtWidgets.QSlider()
        self.slider4.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider4, 4 * 2, NSliderPar)

        self.slider5 = QtWidgets.QSlider()
        self.slider5.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider5, 5 * 2, NSliderPar)

        self.slider6 = QtWidgets.QSlider()
        self.slider6.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider6, 6 * 2, NSliderPar)

        self.slider7 = QtWidgets.QSlider()
        self.slider7.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider7, 7 * 2, NSliderPar)

        self.slider8 = QtWidgets.QSlider()
        self.slider8.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider8, 8 * 2, NSliderPar)

        self.slider9 = QtWidgets.QSlider()
        self.slider9.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider9, 9 * 2, NSliderPar)

        self.slider10 = QtWidgets.QSlider()
        self.slider10.setOrientation(QtCore.Qt.Horizontal)
        grid.addWidget(self.slider10, 10 * 2, NSliderPar)

        ##########
        NSliderConv = 4
        NSliderConvLabel = NSliderConv

        self.LabelShift = QtWidgets.QLabel("Energy Shift")
        grid.addWidget(self.LabelShift, 1*2-1, NSliderConvLabel)
        self.SliderShift = QtWidgets.QSlider()
        self.SliderShift.setOrientation(QtCore.Qt.Horizontal)
        self.SliderShift.setValue(50)
        grid.addWidget(self.SliderShift, 1*2, NSliderConv)

        self.LabelNorm= QtWidgets.QLabel("Normalization Factor")
        grid.addWidget(self.LabelNorm, 2*2-1, NSliderConvLabel)
        self.SliderNorm = QtWidgets.QSlider()
        self.SliderNorm.setOrientation(QtCore.Qt.Horizontal)
        self.SliderNorm.setValue(50)
        grid.addWidget(self.SliderNorm, 2*2, NSliderConv)
        ##########
        self.pushButtonFit = QPushButton("AUTO FIT")
        grid.addWidget(self.pushButtonFit, 1, 5)

        self.setLayout(grid)
        # signal
        self.slider1.sliderReleased.connect(self.cal)
        self.slider2.sliderReleased.connect(self.cal)
        self.slider3.sliderReleased.connect(self.cal)
        self.slider4.sliderReleased.connect(self.cal)
        self.slider5.sliderReleased.connect(self.cal)
        self.slider6.sliderReleased.connect(self.cal)
        self.slider7.sliderReleased.connect(self.cal)
        self.slider8.sliderReleased.connect(self.cal)
        self.slider9.sliderReleased.connect(self.cal)
        self.slider10.sliderReleased.connect(self.cal)
        #
        self.SliderNorm.sliderReleased.connect(self.cal)
        self.SliderShift.sliderReleased.connect(self.cal)
        #
        self.pushButtonFit.clicked.connect(self.fit)
        return None


    def cal_old(self):
        self.getpar()

        par=self.par
        mu=self.f.predict(self.par)
        mu=mu.reshape(mu.shape[1])
        energy=np.loadtxt("IHS_500_energy.txt")
        Gamma_hole = 2.7;
        Ecent = 30;
        Elarg = 50;
        Gamma_max = 11;
        e0 = e0 = 7114.2;
        Efermi = 3 + e0;
        eip, muip = smooth_fdmnes(energy, mu, Gamma_hole, Ecent, Elarg, Gamma_max, Efermi)
        norm=33
        exp=np.loadtxt("exp_excited.txt",skiprows=1)
        print(par)
        plt.close()

        plt.plot(exp[:,0],exp[:,1],'b')
        plt.plot(eip,muip*norm,'r')
        plt.legend(["calculation","experiment"])
        plt.xlim([7100,7200])
        plt.show()
    #     self.retranslateUi(Form)
    #     QtCore.QMetaObject.connectSlotsByName(Form)
    #
    # def retranslateUi(self, Form):
    #     _translate = QtCore.QCoreApplication.translate
    #     Form.setWindowTitle(_translate("Form", "Form"))

#class for test
# class TestMainForm(QMainWindow, Ui_Form):
#     def __init__(self, parent=None):
#         super(TestMainForm, self).__init__(parent)
#         self.setupUi(self)
def main():
    app = QtWidgets.QApplication(sys.argv)
    myWin = QTFITIT()
    myWin.show()
    sys.exit(app.exec_())
def run():
    app = QtWidgets.QApplication(sys.argv)
    myWin = QTFITIT()
    myWin.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()

    # app = QtWidgets.QApplication(sys.argv)
    # myWin = QTFITIT()
    # myWin.show()
    # sys.exit(app.exec_())




    # with open("input.txt") as f:
    #     tmp = f.readline()
    #     tmp = tmp.strip()
    # input = myinput(tmp)
    # aa=input.input_dict['par_name']



