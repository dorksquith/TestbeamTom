#!/usr/bin/python
import ROOT
from ROOT import gDirectory,gPad, gStyle, gROOT, gSystem, gInterpreter, TFile, TF1, TTree, TH2F, TH1F,TH3F, TCanvas,TChain, TVector3, TLegend, Math, TLatex
import numpy as np
gStyle.SetOptStat(1)

import os

fname = "Period234-deltas.root"
f= TFile(fname)

NoCut=True
periods=["P2","P3","P4"]
hypos=["PiMu","Proton"]
cols=[617,797]
dims=["X","Y"]

for i in periods:
    for j in hypos:
        for k in dims:
            varname = "Delta"+k+"Vertex"+j+"_"+i
            oname = "d"+k+'-'+j+'-'+i
            if NoCut:
                varname = "Delta"+k+"Vertex"+j+"NoCut_"+i
                oname = "d"+k+'-'+j+'-NoCut-'+i

            f.cd(varname)
            h=gDirectory.Get("hist")

            c=TCanvas("c","",500,500)
            c.cd()

            h.Scale(1./h.Integral())
            
            h.SetLineWidth(2)
            h.GetXaxis().SetTitle("#Delta "+k+" (BPF-WC) [cm]")
            h.GetXaxis().CenterTitle()
            h.SetMaximum(0.3)

            if j=="PiMu":
                col=619
            else:
                col=808

            if NoCut:
                g = TF1 ( "gf" ,"gaus" ,-20 ,20)
            elif k=="X":
                g = TF1 ( "gf" ,"gaus" ,-3 ,2)
            else:
                g = TF1 ( "gf" ,"gaus" ,-2 ,3)
            g.SetLineWidth(5)
            g.SetLineColor(col)
            
            h.Fit(g,"ER")
            h.DrawCopy("pe")
            chi2 = g.GetChisquare()
            ndof = g.GetNDF ()
            mean = g.GetParameter(1)
            width = g.GetParameter(0)
            latex = ROOT.TLatex ()
            latex.SetNDC()
            latex.SetTextSize (0.04)
            if NoCut:   
                latex.DrawText(0.13 ,0.85 , j+'NC_'+i)
            else:
                latex.DrawText(0.13 ,0.85 , j+'_'+i)    
            latex.SetTextColor (col)
            latex.DrawText(0.13 ,0.80 , " Mean = %.1f cm " %( mean ))
            latex.DrawText(0.13 ,0.75 , " Width = %.1f cm " %( width ))
            latex.DrawLatex(0.13 ,0.7 , " #chi^{2}/n = %.1f " %(
            chi2 / ndof ))
            c.Print(oname+".pdf")
            c.Close()




    
