### AGENT INTELIGENT PENTRU JOCUL ȚINTAR
Țintarul, cunoscut și sub numele de ”Nine men‘s morris”, este un joc de strategie în care doi jucători își plasează piesele pe tablă cu scopul de a forma linii a câte trei piese și de a captura piesele adversarului.

Obiectivul acestei lucrări este de a oferi pasionaților de țintar o variantă digitală prin care să invețe și să avanseze în strategiile jocului. Pentru a atinge acest obiectiv am implementat o interfață grafică unde utilizatorul poate selecta tipul de joc (împotriva unui alt utilizator, împotriva unui agent inteligent sau să vizioneze un joc între doi agenți inteligenți) și poate schimba parametrii agentului inteligent (algoritmul folosit, adâncimea acestuia și euristica folosită). De asemenea, pentru utilizatorii ce vor să joace acest joc pe o tablă reală, există functionalitatea de sincronizare cu ajutorul imaginii redate de o cameră video. Pentru îndeplinirea obiectivului, lucrarea este alcătuită din patru componente realizate în Python:
- Interfața grafică realizată cu ajutorul PySimpleGUI pentru selectarea opțiunilor agentului inteligent și pentru selectarea tipului de joc
- Interfața grafică realizată cu ajutorul PyGame pentru simularea jocului
- Realizarea agentului inteligent ce constă în algoritmul bazat pe paradigma învățării prin recompense, min-max sau varianta accelerată cu alpha-beta, împreună cu opt tipuri de euristici
- Realizarea sincronizării tablei reale cu cea din PyGame:
- Alinierea imaginii redate de camera video folosind descriptori SIFT
- Extragerea de patch-uri ce conțin pozițiile pieselor
- Realizarea unui clasificator ce prezice ce fel de piesă există sau nu într-un patch folosind descriptori ResNet-18 și un model LinearSVC
- Recunoașterea configurației curente pe tabla de joc
Lucrarea se concentrează pe prezentarea celor patru componente și îmbinarea lor în
aplicația finală, precum și pe prezentarea rezultatelor experimental obținute.
