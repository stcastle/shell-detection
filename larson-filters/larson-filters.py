# Source
# ftp://ftp.ster.kuleuven.ac.be/dist/maarten/pieterdg/thesis.pdf
# Routine B.9: Code van de Larson-Slaughter filter.
def larsonSlaughter(bestand,sep,wc,wm,radial_scale): 
    norm=−3;wc=wc/norm;wm=wm/norm #normeer kernel
    data=pyfits.getdata(bestand); 
    center=findOptocenter(bestand)
    transpose(data)
    data=medianFilter(data,3) #voer ruisreductie uit data2=data−data
    for i in range(sep+1,len(data)−sep−1):
        for j in range(sep+1,len(data[0])−sep−1):
            straal=sqrt((center[0]−i)∗∗2.+(center[1]−j)∗∗2.) 
            pix_sep=int(round(sep+straal/radial_scale))
            if i+pix_sep<len(data) and i−pix_sep>0 and j+pix_sep<len(data[0]) and j−pix_sep>0:
                data2[i,j]=data[i,j]/norm−wc∗(data[i+pix_sep,j+pix_sep]+data[i−pix_sep,j−pix_sep]
                + data[i+pix_sep,j−pix_sep]+data[i−pix_sep,j+pix_sep]) 
                − wm∗(data[i−pix_sep,j]+data[i+pix_sep,j]+data[i,j−pix_sep]+data[i,j+pix_sep])
            else: data2[i,j]=0
                transpose(data);transpose(data2) data_diff=data2−data
    return data2,data_diff

# Routine B.10: Code van de Larson-Sekanina filter.
def larsonSekanina(bestand,dr,dtheta): 
    data=pyfits.getdata(bestand); 
    transpose(data) 
    data2=data.copy() 
    center=findOptocenter(bestand) 
    dtheta=deg2rad(dtheta)
    for i in range(0,len(data)):
        for j in range(0,len(data[0])):
            x=float(i−center[0])
            y=float(j−center[1])
            r=sqrt(x∗∗2.+y∗∗2.)
        if r!=0: 
            s=1+dr/r
        else: 
            s=100000
        k1=int(round( s∗cos(dtheta)∗x+s∗sin(dtheta)∗y+center[0])) #opname roteren over hoek theta 
        l1=int(round(−s∗sin(dtheta)∗x+s∗cos(dtheta)∗y+center[1]))
        k2=int(round( s∗cos(−dtheta)∗x+s∗sin(−dtheta)∗y+center[0])) #opname roteren over hoek −theta 
        l2=int(round(−s∗sin(−dtheta)∗x+s∗cos(−dtheta)∗y+center[1]))
        #pixel enkel veranderen als alle nodige getransformeerde pixels binnen het beeldveld liggen:
        if (k1>=0 and k1<len(data)) and (l1>=0 and l1<len(data[0]))
            and ((k2>=0 and k2<len(data)) and (l2>=0 and l2<len(data[0]))):
            data2[i,j]=2∗data[i,j]−data[k1,l1]−data[k2,l2] 
        else:
            data2[i,j]=1
    data2[int(center[0]),int(center[1])]=1;data2[int(center[0]),int(center[1])+1]=1    
    data2[int(center[0]),int(center[1])−1]=1;data2[int(center[0])+1,int(center[1])]=1
    data2[int(center[0])−1,int(center[1])]=1
    transpose(data2)
    return data2
