

var myApp = angular.module('formApp',[ 'multipleSelect', 'ngAnimate', 'ui.bootstrap', 'angularjs-dropdown-multiselect', "checklist-model" ]);

myApp.config(function($httpProvider) {

  $httpProvider.defaults.useXDomain = true;
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
  $httpProvider.defaults.headers.common['Access-Control-Allow-Methods'] = 'POST';
  $httpProvider.defaults.headers.common['Access-Control-Allow-Headers'] = '*';
  console.log("HTTP PROVIDER");
  console.log($httpProvider);

});

myApp.directive('onFileChange', function() {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var onChangeHandler = scope.$eval(attrs.onFileChange);

      element.bind('change', function() {
        scope.$apply(function() {
          var files = element[0].files;
          if (files) {
            onChangeHandler(files);
          }
        });
      });
    }
  };
});

myApp.controller('formCtrl', function($scope, $http, $filter, $timeout){

  $scope.creatingExcel = false;

  $scope.factureDate = "";
  $scope.montant = "";
  $scope.montant2 = "";
	
	$scope.factureFilename = "";
  $scope.repairFactureFilename = "";
  $scope.substitutionFactureFilename = "";
  $scope.loadedFacture = false;
  $scope.loadedRepairFacture = false;
  $scope.loadedSubstitutionFacture = false;

  $scope.searchingDataFacture = false;
  $scope.showFeatures = false;
  $scope.showModele = false;
  $scope.showModele_gfk = false;


  $scope.is_tv = false;
  $scope.is_froid = false;
  $scope.is_telephone = false;
  $scope.is_lave_linge = false;
  $scope.is_seche_linge = false;
  $scope.is_laptop = false;
  $scope.is_gfk_modeles = false;
  $scope.downloading_models = false;
  $scope.exist_models = false;

  $scope.exist_value = false;
  $scope.valeur_neuf_similar = 0;
  $scope.value_reparation = "N/A";
  $scope.reparation_baremo = "N/A";
  $scope.substitution_statistique = "N/A";
  $scope.exist_link_aiude = false;
  $scope.link_aiude = "#";

  $scope.stores_tv = false;
  $scope.stores_frigo = false;
  $scope.stores_cel = false;
  $scope.stores_lapt = false;
  $scope.stores_lave_linge = false;
  $scope.stores_modeles = false;

  $scope.new_modeles = {};
  $scope.modele_selected = {"value": ""};


  $scope.onFilesSelected = function(files) {
    console.log("ON FILES SELECTED");
    $scope.factureFilename = files[0].name;
    $scope.loadedFacture = true;
    $scope.searchingDataFacture = true;
    $("#wrapper-facture-date i").removeClass("sr-only");
    $("#wrapper-facture-boutique i").removeClass("sr-only");
    setTimeout(function(){ 
      console.log("SET TIME OUT");
      $("#wrapper-facture-date i").addClass("sr-only");
      $("#wrapper-facture-boutique i").addClass("sr-only");
      $("#facture-date").val("2017-12-06");
      $("#facture-boutique").val("BOUTIQUE DACHET");
    }, 3000);
  };

  $scope.onFilesSelected2 = function(files) {
    console.log("ON FILES 2 SELECTED");
    $scope.repairFactureFilename = files[0].name;
    $scope.loadedRepairFacture = true;
    $("#wrapper-montant i").removeClass("sr-only");
    $("#wrapper-siren i").removeClass("sr-only");
    setTimeout(function(){ 
      console.log("SET TIME OUT");
      $("#wrapper-montant i").addClass("sr-only");
      $("#wrapper-siren i").addClass("sr-only");
      $("#montant").val(10);
      $("#siren").val("SIREN 1");
    }, 3000);
  };

  $scope.onFilesSelected3 = function(files) {
    console.log("ON FILES 3 SELECTED");
    $scope.substitutionFactureFilename = files[0].name;
    $scope.loadedSubstitutionFacture = true;
    $("#wrapper-montant2 i").removeClass("sr-only");
    $("#wrapper-siren2 i").removeClass("sr-only");
    setTimeout(function(){ 
      console.log("SET TIME OUT");
      $("#wrapper-montant2 i").addClass("sr-only");
      $("#wrapper-siren2 i").addClass("sr-only");
      $("#montant2").val(20);
      $("#siren2").val("SIREN 2");
    }, 3000);
  };

  $scope.getHostName = function(url){
    var match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
      return match[2];
    }
    else {
      return null;
    }
  };

  $scope.getDomain = function(url){
    var hostName = $scope.getHostName(url);
    var domain = hostName;
    
    if (hostName != null) {
        var parts = hostName.split('.').reverse();
        
        if (parts != null && parts.length > 1) {
            domain = parts[1] + '.' + parts[0];
                
            if (hostName.toLowerCase().indexOf('.co.uk') != -1 && parts.length > 2) {
              domain = parts[2] + '.' + domain;
            }
        }
    }
    
    return domain;
  };

  function deactivateForms() {
    $scope.is_tv = false;
    $scope.is_telephone = false;
    $scope.is_froid = false;
    $scope.is_seche_linge = false;
    $scope.is_lave_linge = false;
    $scope.is_laptop = false;
    $scope.is_gfk_modeles = false;
  };

  

  function deactiveFroids(){
    $scope.is_froid_0 = false;
    $scope.is_froid_1 = false;
    $scope.is_froid_2 = false;
    $scope.is_froid_3 = false;
  };
  //Función para mostrar los campos correspondientes dependiendo del tipo de nevera
  function typeRefrigerateur() {

    var selectedBien = $scope.wrapper_tree.current_node.name();

    if (selectedBien == "Réfrigérateur standard" || 
        selectedBien == "Réfrigérateur compact"  ||
        selectedBien == "Réfrigérateurs sans congélateur") { 
        deactiveFroids();      
        $scope.is_froid_0 = true;    
    }
    if (selectedBien == "Réfrigérateur américain" || 
        selectedBien == "Réfrigérateur congélateur en bas" || 
        selectedBien == "Réfrigérateur congélateur en haut"||
        selectedBien == "Réfrigétateur combiné") {
        deactiveFroids();
        $scope.is_froid_1 = true;
    }
    if (selectedBien == "Congélateur armoire" || 
        selectedBien == "Congélateur coffre"  ||
        selectedBien == "Congélateur") {
        deactiveFroids();
        $scope.is_froid_2 = true;
    }    
    if (selectedBien == "Cave à vin service" || 
        selectedBien == "Cave à vin vieillissement" || 
        selectedBien == "Cave à vin multi-températures" ||
        selectedBien == "Cave à vin") {
        deactiveFroids();
        $scope.is_froid_3 = true;
    }

  }

  $scope.SearchFeatures = function(){
                
    $scope.showFeatures = true;
    $scope.selectedList_damage = [];
    $scope.new_modeles = {};

    var selectedBien = SelectedBien();

    if(selectedBien in $scope.links_aiude){
      $scope.link_aiude = $scope.links_aiude[selectedBien];
      $scope.exist_link_aiude = true;
    }else{
      $scope.link_aiude = "#";
      $scope.exist_link_aiude = false;
    }

    if (selectedBien == "Téléviseurs") {
        deactivateForms();
        $scope.is_tv = true;
        $scope.typeBien_damage = $scope.tv_damage;
    } else if (selectedBien == "Téléphonie mobile") {
        deactivateForms();
        $scope.is_telephone = true;
        $scope.typeBien_damage = $scope.telephone_damage;
    } else if (selectedBien == "Sèche-linge----") {
        deactivateForms();
        $scope.is_seche_linge = true;
        $scope.typeBien_damage = $scope.seche_linge_damage;
    } else if (selectedBien == "Réfrigérateurs") {
        deactivateForms();
        typeRefrigerateur();
        $scope.is_froid = true;
        $scope.typeBien_damage = $scope.refrigerateurs_damage;
    } else if (selectedBien == "Laptops") {
      deactivateForms();
      $scope.is_laptop = true;
      $scope.typeBien_damage = $scope.laptop_damage;
     
    } else if (selectedBien == "Lave Linge----") {
        $scope.is_lave_linge = true;
        $scope.typeBien_damage = $scope.lave_linge_damage;
      

     
    } else {
      $scope.downloading_models = true;
      $scope.exist_models = false;
      deactivateForms();
      $scope.is_gfk_modeles = true;

      

      // var data = {
      //   "_type": "reqgfkmodels",
      //   "name": "Peticion de cliente para buscar modelos en GFK",
      //   "country": "1",
      //   "item_category": $scope.categorias_con_ids[selectedBien],
      //   "form_type": $scope.categorias_con_ids[selectedBien],
      //   "data":[{
      //   'Marque': $scope.marcas_con_ids[$scope.marqueSelected]

      //   }]
      // };


      // eliminar luego de las pruebas
      // var prueba1 = {'324542': 'Altic SL 048'};
      // var prueba2 = {'23323': 'Asterie WM 50', '767656': 'Asterie AWM 400'};
      // var prueba3 = {'4545': 'Bellavita LFT 1207 TJV', '342332': 'Bellavita LF 1407 ELED', '434344': 'Bellavita LF 1206 ELE',
      //                '00099': 'Bellavita LFT 1209 TJV', '323232': 'Bellavita LFT 1208 TJV', '231212': 'Bellavita LFT 1006 BKV',
      //                '21212': 'Bellavita LF 1209 BC ITWI', '323211': 'Bellavita LF 1210 BC ITWI', '120565': 'Bellavita LF1208A++BVT',
      //                '87564': 'Bellavita LF 1407 A++ RSCN VT', '43232': 'Bellavita LF 1407 A++ BECN VT', '221056': 'Bellavita LF 1407 A++ NCN',
      //                '12345': 'Bellavita LF 1206 A++ WVET', '986655': 'Bellavita LF 1207 A++ WVET', '232321': 'Bellavita LF 1210 A+++ WVET'};

      // $scope.fakeDownloading = function () {
      //   $timeout(function () {
      //     $scope.downloading_models = false;
      //     $scope.new_modeles = prueba3;
      //   }, 3000);
      // }

      // $scope.fakeDownloading();
      
      // fin eliminar 

      // DESCOMENTAR LUEGO DE LAS PRUEBAS
      var data = {
        "_type": "reqgfkmodels",
        "name": "Peticion de cliente para buscar modelos en GFK",
        "country": "1",
        "item_category": $scope.categorias_con_ids[selectedBien],
        "form_type": $scope.categorias_con_ids[selectedBien],
        "data":[{
        'Marque': $scope.marcas_con_ids[$scope.marqueSelected],
        'Modele': $scope.modele
        }]
      };

    
      var gfkUrl = '/api/gfk/models/';

        var config = {
        headers: {
          'Accept' : 'application/json',
        }
      };

      console.log(data);

      $http.post(gfkUrl, data, config)
      .then (function mySuccess(response){
        interv4 = setInterval(function(){
          var myUrl4 = '/api/gfk/models/'+response.data.job_id+'/';

          var config4 = {
            headers:{
              'Accept' : 'application/json',
            }
          };

          $http.get(myUrl4, config4)
          .then(function mySuccess(response){
            respuesta = response.data;
            console.log(respuesta);

            if(respuesta.status != 'in_progress'){
              clearInterval(interv4);
              $scope.downloading_models = false;

              if(respuesta.status == 'failed'){

                //show_modal_status('failed')
                //TEMPORARY
                alert("Error en busqueda de modelos")

              }else if(respuesta.exist_models){

                $scope.exist_models = true;

                var ma_temp_models = respuesta.models[0]["ma_temp_models"]

                ma_temp_models.forEach(function(obj_model){
                  $scope.new_modeles[obj_model["id_model"]] = obj_model["name_model"]
                });

              }else {
                //show_modal_failed('completed')
                alert("No se obtuvieron resultados")
              }

            }

          }, function myError(response){
              $scope.Resp = response.statusText;
              console.log('MAL3');
              console.log($scope.Resp);
          });

        },3000);
      }, function myError(response){
        $scope.Resp = response.statusText;
        $scope.downloading_models = false;
        console.log('MAL');
        console.log($scope.Resp);
      });
      // FIN DESCOMENTAR

    }
    
   
          
  };
 
  $scope.combineResolution = function(){
    $scope.telephoneResolutionSelected = $scope.telephoneResolutionSelected_1+'x'+$scope.telephoneResolutionSelected_2;
  };
  $scope.initPouce = function(){
    $scope.taillePouce = 55;
    $scope.setCM();
  };

  $scope.setCM = function(){
    $scope.tailleCM = Math.round($scope.taillePouce*2.54);
    $scope.telephone_tailleCM = Math.round($scope.telephone_taillePouce*2.54);
  };
  

  $scope.setPouce = function(){
    $scope.taillePouce = Math.round($scope.tailleCM/2.54);
    $scope.telephone_taillePouce = Math.round($scope.telephone_tailleCM/2.54);
  };

  $scope.ClickSuivant = function() {
    
    $('#tele-evaluation-tab').removeClass('active');
    $('#tele-evaluation').removeClass('active');

    $('#evaluation-tab').addClass('active');
    $('#evaluation').addClass('active');

    if ($scope.valeur_neuf_similar >= $scope.substitutionAssure ){

         $scope.diference = (($scope.valeur_neuf_similar - $scope.substitutionAssure)/$scope.substitutionAssure)*100;
         if ($scope.diference >= 10){
          $('#substitution-assure').removeClass('value-color-orange');
          $('#substitution-assure').addClass('value-color-green');
          $('#model-value').removeClass('value-color-green');
          $('#model-value').addClass('value-color-orange');
         }
          
    };  

  };

  $scope.ClickSuivant1 = function() {
    $('#nouvelle-mission-tab').removeClass('active');
    $('#nouvelle-mission').removeClass('active');

    $('#identification-bien-tab').addClass('active');
    $('#identification-bien').addClass('active');
  };

  $scope.isNotCaveFroid = true;
  $scope.setFroid = function(selectedFroid) {

    $scope.isNotCaveFroid = true;
    if (selectedFroid == $scope.froids_type[0]){

      $scope.froids_subtype = $scope.froids_subtype_1;

    }else if (selectedFroid == $scope.froids_type[1]){

      $scope.froids_subtype = $scope.froids_subtype_2;

    }else if (selectedFroid == $scope.froids_type[2]){

      $scope.froids_subtype = $scope.froids_subtype_3;

    }else if (selectedFroid == $scope.froids_type[3]){

      $scope.froids_subtype = $scope.froids_subtype_4;
      $scope.isNotCaveFroid = false;

    }
// ['Réfrigérateur sans congélateur', 'Congélateur', 'Réfrigétateur combiné', 'Cave à vin'];
  };

// ======================================= JSON RESPONSE =======================================//
  
  //Inicializando valores por defecto:
  //========ALL==============
  $scope.marqueSelected = "";
  $scope.modele = "";
  //========TV==============
  $scope.autresMarques = "" ;
  $scope.taillePouce = 0;
  $scope.tailleCM = 0;
  $scope.type = "" ;
  $scope.resolution = "" ;
  $scope.refresh = "" ;
  $scope.Selected3D = "" ;
  $scope.hdrSelected = "" ;
  $scope.internet = "" ;
  $scope.wifiIntegre  = "" ;
  $scope.smart = "" ;       
  $scope.ratioSelected = "" ;
  $scope.colorSelected = "" ;
  $scope.typePannelSelected = "" ;
  $scope.framerateSelected = "" ;
  $scope.designSelected = "" ;
  $scope.energySelected = "" ;
  //=========TELEPHONE=============
  $scope.telephoneSystemSelected = "";
  $scope.telephone_taillePouce = "";
  $scope.telephoneResolutionSelected = "";
  $scope.telephoneMemorySelected = "";
  $scope.telephoneRamSelected = "";
  $scope.telephoneCoreSelected = "";
  $scope.telephone_megapixel_front = "";
  $scope.telephone_megapixel_back = "";
  $scope.telephoneCouleurSelected = "";
  $scope.telephone_battery = "";
  $scope.telephone_date = "";
  $scope.telephone_prix = "";
  //=========LAVE LINGE=============
  $scope.type_lavelinge = "";
  $scope.marqueSelected = "";
  $scope.modele = "";
  $scope.typeCharge_lavelinge = "";
  $scope.coleur_lavelinge = "";
  $scope.haut = "";
  $scope.largeur = "";
  $scope.profounder = "";
  $scope.typePose_lavelinge = "";
  $scope.tpm = "";
  $scope.chargerKg = "";
  $scope.dcB = "";
  $scope.sechage = "";
  $scope.typeSechoir = "";
  $scope.capaciteSechage = "";
  $scope.niveauBrut = "";
  $scope.consomm_energie = "";
  $scope.consommation = "";
  $scope.cons_eau = "";
  $scope.display = "";
  $scope.programLavage = "";
  //=========FROID=============  
  $scope.selectedFroid = "";
  $scope.froidSubSelected = "";
  $scope.froid_hauteur = { value : ""};
  $scope.froid_largeur = { value : ""};
  $scope.froid_profondeur = { value : ""};
  $scope.froid_volume_utile = { value : ""};
  $scope.poseFroidSelected = { value : ""};
  $scope.froidCouleurSelected = "";
  $scope.energyFroidSelected = { value : ""};
  $scope.froidSystemSelected = { value : ""};
  $scope.froid_type_refrigeration = { value : ""};
  $scope.froidConsommationSelected = { value : ""};
  $scope.froid_volume_utile_refrigerateur = { value : ""};
  $scope.froid_volume_net = { value : ""};
  $scope.froid_volume_net_refrigerateur = { value : ""};
  $scope.froid_volume_utile_congelateur = { value : ""};
  $scope.froid_volume_net_congelateur = { value : ""};
  $scope.froid_volume_total_utile = { value : ""};
  $scope.froid_volume_total_net = { value : ""};
  $scope.froid_volume_utile_2 = { value : ""};
  $scope.froid_volume_net_2_and_3 = { value : ""};
  $scope.froid_Stockage = { value : ""};
  $scope.froid_type_congelation = { value : ""};
  $scope.froid_technologie = { value : ""};

  //=========LAPTOP=============  
  $scope.marqueSelected = "";
  $scope.specCPU = "";
  $scope.gpu = "";
  $scope.modele = "";
  $scope.laptop_proprietes_model = "";
  $scope.taille = "";
  $scope.resolution = "";
  $scope.specRam = "";
  $scope.coeursCPU = "";
  $scope.type_stockage = "";
  $scope.tailleHdd = "";
  $scope.tailleSsd = "";
  $scope.laptop_sortie_video_model = "";
  $scope.lecteur = { value : ""};
  $scope.systeme = "";

  $scope.SendJson = function(){
  
    $scope.jsonResponse = {

       "AutresMarques": "Non",
       "Marque": $scope.marqueSelected,
       "Modele": $scope.modele,
       "TaillePounce":  $scope.taillePouce ,
       "TailleCm":  $scope.tailleCM, 
       "Type":  $scope.type ,
       "Resolution": [ $scope.resolution ],
       "Refresh":  $scope.refresh ,
       "Indice_refresh": $scope.indiceRefresh ,
       "3D": $scope.Selected3D ,
       "HDR": [ $scope.hdrSelected ],

       "Internet":  $scope.internet ,
       "Wifi":  $scope.wifiIntegre  ,
       "Smart":  $scope.smart ,


       "Ratio": [ $scope.ratioSelected ],
       "Couleur": $scope.colorSelected,
       "PannelType": [$scope.typePannelSelected],
       "Framerate": [$scope.framerateSelected],
       "Design": [$scope.designSelected],
       "Energy": $scope.energySelected,   
       
    }
    
  }

  // =======================================SEND JSON RESPONSE =======================================//

  $scope.SendData = function () {


    $('#identification-bien-tab').removeClass('active');
    $('#identification-bien').removeClass('active');

    $('#tele-evaluation-tab').addClass('active');
    $('#tele-evaluation').addClass('active'); 
    

    if(!$scope.marqueSelected){
      $scope.marqueSelected = "" ;
    };
    if(!$scope.modele){
      $scope.modele = "";
    };
    if(!$scope.indiceRefresh){
      $scope.indiceRefresh = "" ;
    };

    var selectedBien = SelectedBien();
    var is_other_case = false;
    
    switch(selectedBien) {
      case "Téléviseurs":

        $scope.stores_tv = true;
        $scope.stores_frigo = false;
        $scope.stores_cel = false;
        $scope.stores_lapt = false;
        $scope.stores_lave_linge = false;
        
        $scope.jsonResponse = {

          "_type": "reqrv",
          "name": "Peticion de cliente para valoracion de producto",
          "country": "1",
          "item_category": "TV_000",
          "form_type": "TV_000",
          "data":[{

             "Marque": $scope.marqueSelected,
             "Modele": $scope.modele,
             "TaillePounce":  String($scope.taillePouce) ,
             "TailleCm":  String($scope.tailleCM) , 
             "Type":  $scope.type ,
             "Resolution": [ $scope.resolution ],
             "Refresh":  $scope.refresh ,
             "Indice_refresh": $scope.indiceRefresh ,
             "3D": $scope.Selected3D ,
             "HDR": [ $scope.hdrSelected ],

             "Internet":  $scope.internet ,
             "Wifi":  $scope.wifiIntegre  ,
             "Smart":  $scope.smart ,


             "Ratio": [ $scope.ratioSelected ],
             "Couleur": $scope.colorSelected,
             "PannelType": [$scope.typePannelSelected],
             "Framerate": [$scope.framerateSelected],
             "Design": [$scope.designSelected],
             "Energy": $scope.energySelected,

            }]
            
        }
        
        break;
      case "Téléphonie mobile":

        $scope.stores_tv = false;
        $scope.stores_frigo = false;
        $scope.stores_cel = true;
        $scope.stores_lapt = false;
        $scope.stores_lave_linge = false;
        
        $scope.jsonResponse = {

          "_type": "reqrv",
          "name": "Peticion de cliente para valoracion de producto",
          "country": "1",
          "item_category": "TLF_000",
          "form_type": "TLF_000",
          "data":[{

              'Type': 'Mobile',
              'Marque': $scope.marqueSelected,
              'Modele': $scope.modele,
              'Systeme dexploitation': $scope.telephoneSystemSelected,
              'Taille': String($scope.telephone_taillePouce),
              'Resolution': $scope.telephoneResolutionSelected,
              'Memoire': String($scope.telephoneMemorySelected),
              'Ram': String($scope.telephoneRamSelected),
              'Coeurs': $scope.telephoneCoreSelected,
              'MegapixelsFrontale': String($scope.telephone_megapixel_front),
              'MegapixelsArriere': String($scope.telephone_megapixel_back),
              'Couleur': $scope.telephoneCouleurSelected,
              'CapaciteBatterie': String($scope.telephone_battery),
              'Date achat': $filter('date')($scope.telephone_date, "yyyy-MM-dd"),
              'Prix achat': String($scope.telephone_prix)

            }]
        }
        
        break;
      case "Laptops":


        //Colocando variable GPU
        var str = $scope.gpu;
        var laptop_gpu_type;
        if (str.search("Intel") >= 0) { laptop_gpu_type = "Integrated";          
        }else {                   laptop_gpu_type = "Dedicated";}
         
        //Colocando variable CPU
        var str2 = $scope.specCPU;
        var laptop_cpu_type;
        if       (str2.search("Intel Core i7") >= 0){ laptop_cpu_type = "Intel Core i7";
        }else if (str2.search("Intel Core i5") >= 0){ laptop_cpu_type = "Intel Core i5";
        }else if (str2.search("Intel Core i3") >= 0){ laptop_cpu_type = "Intel Core i3";
        }else if (str2.search("Intel Core M") >= 0) { laptop_cpu_type = "Intel Core M";
        }else if (str2.search("Intel Pentium") >= 0){ laptop_cpu_type = "Intel Pentium";
        }else if (str2.search("Intel Celeron") >= 0){ laptop_cpu_type = "Intel Celeron";
        }else if (str2.search("Intel Atom") >= 0)   { laptop_cpu_type = "Intel Atom";
        }else if (str2.search("AMD A-series") >= 0) { laptop_cpu_type = "AMD A-series";
        }else if (str2.search("AMD E-series") >= 0) { laptop_cpu_type = "AMD E-series";
        }else if (str2.search("AMD Fusion") >= 0)   { laptop_cpu_type = "AMD Fusion";
        }else {                                       laptop_cpu_type = "";};


        console.log(laptop_cpu_type);
        console.log($scope.specCPU);


        $scope.stores_tv = false;
        $scope.stores_frigo = false;
        $scope.stores_cel = false;
        $scope.stores_lapt = true;
        $scope.stores_lave_linge = false;
        
        $scope.jsonResponse = {

            "_type": "reqrv",
            "name": "petición de valorizacion",
            "country": '1',
            "item_category": 'COMPU_000',
            "form_type": 'COMPU_000',
            "data": [{
            'Type' : 'Laptop',
            'Marque' : $scope.marqueSelected,
            'CPU' : laptop_cpu_type,
            'CPUSpec' : $scope.specCPU,
            'GPU' : laptop_gpu_type,
            'GPUSpec' : $scope.gpu,
            'Modele' : $scope.modele,
            'Proprietes' : $scope.laptop_proprietes.values,
            'Taille (pounce)' : $scope.taille,
            'Resolution' : $scope.resolution,
            'Ram (Go)' : $scope.specRam,
            'Coeurs CPU' : $scope.coeursCPU,
            'Type de stockage' : $scope.type_stockage,
            'Taille HDD (Go)' : $scope.tailleHdd,
            'Taille SSD (Go)' : $scope.tailleSsd,
            'Sortie video' : $scope.laptop_sortie_video.values,
            'Lecteur/Graveur' : $scope.lecteur.value,
            "Systeme dexploitation" : $scope.systeme
            }]
          
          }
          
          break;
      case "Lave Linge----":

        $scope.stores_tv = false;
        $scope.stores_frigo = false;
        $scope.stores_cel = false;
        $scope.stores_lapt = false;
        $scope.stores_lave_linge = true;
        
        $scope.jsonResponse = {

          "_type": "reqrv",
          "name": "petición de valorizacion",
          "country": '1',
          "item_category": 'LAVE_000',
          "form_type": 'LAVE_000',
          "data": [{
          'Type' : $scope.type_lavelinge,
          'Marque': $scope.marqueSelected,
          'Modele': $scope.modele,
          'Type charge' : $scope.typeCharge_lavelinge,
          'Coleur' : $scope.coleur_lavelinge,
          'Haut' : $scope.haut,
          'Largeur' : $scope.largeur,
          'Profounder' : $scope.profounder,
          'Type Pose' : $scope.typePose_lavelinge,
          'Vitesse dessorage maximale (tpm)': $scope.tpm,
          'Capacité de chargement (kg)' : $scope.chargerKg,
          'Niveau de bruit centrifuge (dcB)' : $scope.dcB,
          'Fonction de séchage' : $scope.sechage,
          'Type Séchoir' : $scope.typeSechoir,
          'Capacité de séchage (kg)' : $scope.capaciteSechage,
          'Niveau de bruit sec (dcB)' : $scope.niveauBrut,
          'Consommation dénergie' : $scope.consomm_energie,
          'Consommation (kWh/an)' : $scope.consommation,
          'Consommation deau (litres)' : $scope.cons_eau,
          'Display' : $scope.display,
          'Programmes de lavage': $scope.programLavage
          }]
          
        }
        
        break;
      case "Réfrigérateurs":

        $scope.stores_tv = false;
        $scope.stores_frigo = true;
        $scope.stores_cel = false;
        $scope.stores_lapt = false;
        $scope.stores_lave_linge = false;

        $scope.jsonResponse = JsonRefrigerateur();

        
        break;
      default:

        is_other_case = true;
      
    }
    
    if (!is_other_case) {


      var data = $scope.jsonResponse; 
      console.log(data);
       
      var myUrl = '/api/results-valuation/'; //'http://ec2-34-238-120-34.compute-1.amazonaws.com/comparador/';

      console.log("JSON REQUEST");
      console.log($scope.jsonResponse);

      var config = {
        headers: {
          'Accept' : 'application/json',
        }
      };

      $http.post(myUrl, data, config)
      .then(function mySuccess(response) {
          $scope.Resp = response.data;
          console.log($scope.Resp);
          console.log('BIEN');

          $scope.creatingExcel = true;
          $scope.exist_value = false;
          $scope.valeur_neuf_similar = 0;
          $scope.value_reparation = "N/A";
          $scope.reparation_baremo = "N/A";
          $scope.substitution_statistique = "N/A";


          interv2 = setInterval(function(){

            var myUrl3 = '/api/urls-generated/'+response.data.job_id+'/'; //https://mavalue.herokuapp.com      'http://ec2-34-238-120-34.compute-1.amazonaws.com/obtener-resultado/';

            var config3 = {
              headers: {
                'Accept' : 'application/json',
              }
            };

            $http.get(myUrl3, config3)
            .then(function mySuccess(response) {

              respuesta = response.data;

              if(respuesta.existe_urls){

                clearInterval(interv2);

                $scope.store_urls = {}
                
                for(index in respuesta.urls){
                  link = respuesta.urls[index]
                  $scope.store_urls[$scope.getDomain(link)] = link;

                }
               
              }

            }, function myError(response) {
              $scope.Resp = response.statusText;
              console.log('Error en busqueda de urls de tiendas');
            });

          },3000);



          interv = setInterval(function(){

            var myUrl2 = '/api/results-valuation/'+response.data.job_id+'/'; //https://mavalue.herokuapp.com      'http://ec2-34-238-120-34.compute-1.amazonaws.com/obtener-resultado/';

            var config2 = {
              headers: {
                'Accept' : 'application/json',
              }
            };

            var data2 = {
              token: "jdhYD98S98",
            };

            $http.get(myUrl2, config2)
            .then(function mySuccess(response) {

              respuesta = response.data;

              if(!$scope.creatingExcel){
                $scope.creatingExcel = true;
              }

              console.log(respuesta);

              if(respuesta.status != 'in_progress'){

                clearInterval(interv);
                $scope.creatingExcel = false;

                if(respuesta.status == 'failed'){

                  //show_modal_failed('failed')
                  //TEMPORARY
                  alert("Problemas durante proceso de Valorizacion")

                }else if(respuesta.existe_excel){


                  respuesta.job_data.forEach(
                    function(obj){
                      if("precio_minimo" in obj){
                        $scope.valeur_neuf_similar = obj.precio_minimo;
                        $scope.exist_value = true;
                      }

                      if("resultado_reparation" in obj){
                        $scope.value_reparation = obj.resultado_reparation + ' €';
                      }

                      if("resultado_segunda_mano" in obj){
                        $scope.substitution_statistique = obj.resultado_segunda_mano + ' €';
                      }

                      if("resultado_reparation_baremo" in obj){
                        $scope.reparation_baremo = obj.resultado_reparation_baremo;
                        if($scope.reparation_baremo != "Indisponible"){
                          $scope.reparation_baremo = $scope.reparation_baremo + ' €';
                        }
                      }
                    }
                  );

                  var url = respuesta.url;
                  $('a#link-excel').attr({href : url});

                }

              }


            }, function myError(response) {
              $scope.Resp = response.statusText;
              $scope.creatingExcel = false;
              console.log('Error en proceso de Valorizacion');
              console.log($scope.Resp);
            });

          },10000);

        }, function myError(response) {
            $scope.Resp = response.statusText;
            console.log('Error en peticion de valorizacion');
            console.log($scope.Resp);

        });


    } else {

        if(!$scope.modele_selected.value){
          return;
        }

        var data = {
          "_type": "reqgfkmodels",
          "name": "Peticion de cliente para buscar modelos en GFK",
          "country": "1",
          "item_category": $scope.categorias_con_ids[selectedBien],
          "form_type": $scope.categorias_con_ids[selectedBien],
          "data":[{
          'Marque': $scope.marcas_con_ids[$scope.marqueSelected],
          'Modele': $scope.modele_selected.value
          }]
        };

        var myUrl = '/api/results-valuation/'; //'http://ec2-34-238-120-34.compute-1.amazonaws.com/comparador/';


        var config = {
          headers: {
            'Accept' : 'application/json',
          }
        };

        $http.post(myUrl, data, config)
        .then(function mySuccess(response) {

          $scope.creatingExcel = true;
          $scope.valeur_neuf_similar = 0;
          $scope.value_reparation = "N/A";
          $scope.reparation_baremo = "N/A";
          $scope.substitution_statistique = "N/A";

          interv = setInterval(function(){

            var myUrl2 = '/api/results-valuation/'+response.data.job_id+'/'; //https://mavalue.herokuapp.com      'http://ec2-34-238-120-34.compute-1.amazonaws.com/obtener-resultado/';

            var config2 = {
              headers: {
                'Accept' : 'application/json',
              }
            };

            $http.get(myUrl2, config2)
            .then(function mySuccess(response) {

              respuesta = response.data;

              if(!$scope.creatingExcel){
                $scope.creatingExcel = true;
              }

              console.log(respuesta);

              if(respuesta.status != 'in_progress'){
                clearInterval(interv);
                $scope.creatingExcel = false;

                if(respuesta.status == 'failed'){

                  //show_modal_failed('failed')
                  //TEMPORARY
                  alert("Problemas durante proceso de Valorizacion")

                }else if(respuesta.existe_excel){
                  var url = respuesta.url;
                  $('a#link-excel').attr({href : url});
                }else {
                  //show_modal_failed('completed')
                  alert("No se obtuvieron resultados")
                }               

              }

            }, function myError(response) {
              $scope.Resp = response.statusText;
              $scope.creatingExcel = false;
              console.log('Error en proceso de Valorizacion');
              console.log($scope.Resp);
            });

          },10000);


        }, function myError(response) {
            $scope.Resp = response.statusText;
            console.log('Error en peticion de Valorizacion');
            console.log($scope.Resp);

        });
        
    }

    

  };

  function SelectedBien(){
    var selectedBien = $scope.wrapper_tree.current_node.name();

    //Dectectar si es algun tipo de refrigerador
    if (selectedBien == "Réfrigérateur standard" || 
        selectedBien == "Réfrigérateur compact" ||
        selectedBien == "Congélateur armoire" || 
        selectedBien == "Congélateur coffre" ||
        selectedBien == "Réfrigérateur américain" || 
        selectedBien == "Réfrigérateur congélateur en bas" || 
        selectedBien == "Réfrigérateur congélateur en haut" ||
        selectedBien == "Cave à vin service" || 
        selectedBien == "Cave à vin vieillissement" || 
        selectedBien == "Cave à vin multi-températures" ||
        selectedBien == "Réfrigérateurs sans congélateur" ||
        selectedBien == "Réfrigétateur combiné" ||
        selectedBien == "Congélateur" ||
        selectedBien == "Cave à vin"  ) {
        
          selectedBien = "Réfrigérateurs";
    }
   

    return selectedBien;
  }

  function JsonRefrigerateur(){
    var selectedBien = $scope.wrapper_tree.current_node.name();
    var jsonRefrigerateur;
    if (selectedBien == "Réfrigérateur standard" || 
        selectedBien == "Réfrigérateur compact"  ||
        selectedBien == "Réfrigérateurs sans congélateur" ) {
        
      jsonRefrigerateur = {

          "_type": "reqrv",
          "name": "Peticion de cliente para valoracion de producto",
          "country": "1",
          "item_category": "FRIGO_000",
          "form_type": "FRIGO_000",
          "data":[{

              'Marque': $scope.marqueSelected,
              'Modele': $scope.modele,
              'Subtype': selectedBien,
              'Hateur': $scope.froid_hauteur.value,
              'Largeur': $scope.froid_largeur.value,
              'Profoundeur': $scope.froid_profondeur.value,
              'Volume utile': $scope.froid_volume_utile.value,
              'Volume net': $scope.froid_volume_net.value,
              'TypePose': $scope.poseFroidSelected.value,
              'Couleur': $scope.froidCouleurSelected,
              'Systeme de froid' : $scope.froidSystemSelected.value,
              'Energy': $scope.energyFroidSelected.value,
              'Consommation' : $scope.froidConsommationSelected.value,

            }]
        }



    }
   
    if (selectedBien == "Congélateur armoire" || 
        selectedBien == "Congélateur coffre"  ||
        selectedBien == "Congélateur") {
          jsonRefrigerateur = {
            "_type": "reqrv",
            "name": "petición de valorizacion",
            "country": '1',
            "item_category": 'FRIGO_002',
            "form_type": 'FRIGO_002',
            "data": [{
            'Marque' : $scope.marqueSelected,
            'Modele' : $scope.modele,
            'Subtype' : selectedBien,
            'Hateur' : String($scope.froid_hauteur.value),
            'Largeur' : String($scope.froid_largeur.value),
            'Profoundeur' : String($scope.froid_profondeur.value),
            'Volume utile' : $scope.froid_volume_utile_2.value,
            'Volume net' : $scope.froid_volume_net_2_and_3.value,
            'TypePose' : $scope.poseFroidSelected.value,
            'Energy' : $scope.energyFroidSelected.value,
            'Couleur' : $scope.froidCouleurSelected,
            'Systeme de froid' : $scope.froidSystemSelected.value,
            'Consommation' : $scope.froidConsommationSelected.value,
            }]
            }
    }
    if (selectedBien == "Réfrigérateur américain" || 
        selectedBien == "Réfrigérateur congélateur en bas" || 
        selectedBien == "Réfrigérateur congélateur en haut"||
        selectedBien == "Réfrigétateur combiné") {
          jsonRefrigerateur = {
            "_type": "reqrv",
            "name": "petición de valorizacion",
            "country": '1',
            "item_category": 'FRIGO_001',
            "form_type": 'FRIGO_001',
            "data": [{
            'Marque' : $scope.marqueSelected,
            'Modele' : $scope.modele,
            'Subtype' : selectedBien,
            'Hateur' : String($scope.froid_hauteur.value),
            'Largeur' : String($scope.froid_largeur.value),
            'Profoundeur' : String($scope.froid_profondeur.value),
            'Volume utile frigo': $scope.froid_volume_utile_refrigerateur.value,
            'Volume net frigo': $scope.froid_volume_net_congelateur.value,
            'Volume utile congelateur': $scope.froid_volume_utile_congelateur.value,
            'Volume net congelateur': $scope.froid_volume_net_refrigerateur.value,
            'Volume utile' : $scope.froid_volume_total_utile.value,
            'Volume net' : $scope.froid_volume_total_net.value,
            'TypePose' : $scope.poseFroidSelected.value,
            'Energy' : $scope.energyFroidSelected.value,
            'Couleur' : $scope.froidCouleurSelected,
            'Type refrigeration' : $scope.froid_type_refrigeration.value,
            'Type congelation' : $scope.froid_type_congelation.value,
            'Technologie' : $scope.froid_technologie.value,
            'Display' : $scope.froid_display,
            'Dispenseur' : $scope.froid_dispenseur,
            'Consommation' : $scope.froidConsommationSelected.value,
            }]
            }
    }
    if (selectedBien == "Cave à vin service" || 
        selectedBien == "Cave à vin vieillissement" || 
        selectedBien == "Cave à vin multi-températures" ||
        selectedBien == "Cave à vin"){
          jsonRefrigerateur = {
            "_type": "reqrv",
            "name": "petición de valorizacion",
            "country": '1',
            "item_category": 'FRIGO_003',
            "form_type": 'FRIGO_003',
            "data": [{
            'Marque' : $scope.marqueSelected,
            'Modele' : $scope.modele,
            'Subtype' : selectedBien,
            'Hateur' : String($scope.froid_hauteur.value),
            'Largeur' : String($scope.froid_largeur.value),
            'Profoundeur' : String($scope.froid_profondeur.value),
            'Stockage' : $scope.froid_Stockage.value,
            'Volume net' : $scope.froid_volume_net_2_and_3.value,
            'TypePose' : $scope.poseFroidSelected.value,
            'Energy' : $scope.energyFroidSelected.value,
            'Couleur' : $scope.froidCouleurSelected,
            'Systeme de froid' : $scope.froidSystemSelected.value,
            'Consommation' : $scope.froidConsommationSelected.value,
            }]
            }

    }
     console.log(jsonRefrigerateur);
  return jsonRefrigerateur;
  }

  

  // ======================================= MULTIPLETSELECT LIST ===========================================//

  /* ITEMS TREE */
  $scope.typeBienTree = [
    {
      name: "Multimedia (Brun)",
      children: [
        {
          name: "Image et home cinéma",
          children: [
            {
              name: "Téléviseurs"
            },
            {
              name: "Lecteur DVD"
            },
            {
              name: "Data/Video-Projecteurs"
            }
          ]
        },
        {
          name: "Audio et hifi",
          children: [
            {
              name: "Radio/Radio-réveil"
            },
            {
              name: "Casques"
            },
            {
              name: "Kits Oreillette"
            }
          ]
        },
      ]
    },

    {
      name: "Gros electromenagers (Blanc)",
      children: [
        {
          name: "Lavage",
          children: [
            {
              name: "Lave Linge"
            },
            {
              name: "Sèche Linge"
            },
            {
              name: "Lave Vaisselle"
            }
          ]
        },
        {
          name: "Froid",
          children: [
            {
              name: "Réfrigérateurs sans congélateur",
              children: [
                {
                  name: "Réfrigérateur standard"
                },
                {
                  name: "Réfrigérateur compact"
                }
              ]
            },
            {
              name: "Congélateur",
              children: [
                {
                  name: "Congélateur armoire"
                },
                {
                  name: "Congélateur coffre"
                }
              ]
            },
            {
              name: "Réfrigétateur combiné",
              children: [
                {
                  name: "Réfrigérateur américain"
                },
                {
                  name: "Réfrigérateur congélateur en bas"
                },
                {
                  name: "Réfrigérateur congélateur en haut"
                }
              ]
            },
            {
              name: "Cave à vin",
              children: [
                {
                  name: "Cave à vin service"
                },
                {
                  name: "Cave à vin vieillissement"
                },
                {
                  name: "Cave à vin multi-températures"
                }
              ]
            }
          ]
        },
        {
          name: "Cuisson",
          children: [
            {
              name: "Cuisinière et Four"
            },
            {
              name: "Mini Fours"
            },
            {
              name: "Plaques de Cuisson"
            },
            {
              name: "Tireuse à Bière"
            },
            {
              name: "Hottes"
            },
            {
              name: "Robots"
            }
          ]
        }
      ]
    },
    {
      name: "Petit Electroménager",
      children: [
        {
          name: "Cafetière et Expresso"
        },
        {
          name: "Repassage",
          children: [
            {
              name: "Fer à Repasser"
            }
          ]
        },
        {
          name: "Aspirateurs"
        }
      ]
    },
    {
      name: "Informatique et Nomade (Gris)",
      children: [
        {
          name: "Informatique",
          children: [
            {
              name: "Laptops"
            },
            {
              name: "Desktops/Serveurs"
            },
            {
              name: "Multifonctions (MFD)"
            },
            {
              name: "Enceintes PC / Stations MP3"
            },
            {
              name: "Disques Durs"
            },
            {
              name: "Moniteurs"
            }                    
          ]
        },
        {
          name: "Téléphonie et tablette (Nomade)",
          children: [
            {
              name: "Téléphonie mobile"
            },
            {
              name: "Tablette"
            }
          ]
        },
        {
          name: "Jeux vidéos",
          children: [
            {
              name: "Consoles de jeu"
            }
          ]
        },
        {
          name: "Photo et video",
          children: [
            {
              name: "Appareils Photo Numériques"
            },
            {
              name: "Camescopes"
            }
          ]
        },
        {
          name: "Baladeur Numérique (MP3/MP4)"
        },
        {
          name: "Navigation Embarquée"
        },
        {
          name: "Réception satellite"
        }
      ]
    }
    // {
    //   name: "Immobilier - Maisom",
    //   children: [
    //     {
    //       name: "Maison",
    //       children: [
    //         {
    //           name: "Chauffage - Plomberie",
    //           children: [
    //             {
    //               name: "Chaudière de toute nature"
    //             },
    //             {
    //               name: "Chauffe-eau (à résistance ou thermodynamique)"
    //             },
    //             {
    //               name: "Circulateur d'air chaud (y compris pur un insert de cheminée)"
    //             },
    //             {
    //               name: "Climatiseur fixe (y compris split system)"
    //             },
    //             {
    //               name: "Ballon d'eau chaude"
    //             },
    //             {
    //               name: "Cumulus"
    //             },
    //             {
    //               name: "Convecteur ou radiateur électrique (y compris panneaux rayonnants muraux ou en plafond, câbles chauffants en sol ou extérieurs"
    //             },
    //             {
    //               name: "Adoucisseur d'eau"
    //             },
    //             {
    //               name: "Vannes motorisées (chauffage)"
    //             },
    //             {
    //               name: "Pompe de forage pour alimenter habitation et jardin"
    //             },
    //             {
    //               name: "Pompe de relevage"
    //             },
    //             {
    //               name: "Pompe à chaleur de toute nature"
    //             },
    //             {
    //               name: "Poêle à bois à granulé"
    //             },
    //             {
    //               name: "Installation photovoltaïque et ses accessoires (panneaux, câblage, onduleurs)"
    //             }                 
    //           ]
    //         },
    //         {
    //           name: "Electricité",
    //           children: [
    //             {
    //               name: "Disjoncteur électrique (disjoncteur principal, tableau de distribution et ses organes de sécurité, transformateurs, …)"
    //             },
    //             {
    //               name: "Eclairage extérieur solidaire aux bâtiments assurés"
    //             },
    //             {
    //               name: "Ligne électrique (y compris téléphonique et informatique)"
    //             },
    //             {
    //               name: "Prise électrique"
    //             },
    //             {
    //               name: "Tableau électrique"
    //             },
    //             {
    //               name: "Borne recharge voiture électrique (prise électrique précédée d'un redresseur / transformateur)"
    //             }                  
    //           ]
    //         },
    //         {
    //           name: "Meunuiseries électriques",
    //           children: [
    //             {
    //               name: "Porte de garage motorisée"
    //             },
    //             {
    //               name: "Portail motorisé"
    //             },
    //             {
    //               name: "Alarme (détecteur et centrale)"
    //             },
    //             {
    //               name: "Amplificateur électrique (ampli d'antenne)"
    //             },
    //             {
    //               name: "Antenne et parabole (motorisation)"
    //             },
    //             {
    //               name: "Aspirateur centralisé"
    //             },
    //             {
    //               name: "Ascenseur (parties électriques)"
    //             },
    //             {
    //               name: "Clôture électrique"
    //             },
    //             {
    //               name: "Domotique"
    //             },
    //             {
    //               name: "Eolienne (si elle a pour fonction l’alimentation de l’habitation et seule une partie est électrique)"
    //             },
    //             {
    //               name: "Hotte aspirante (sauf cas particuliers d’hottes non encastrées et facilement démontables)"
    //             },
    //             {
    //               name: "Interphone"
    //             },
    //             {
    //               name: "Monte escalier (partie électrique)"
    //             },
    //             {
    //               name: "Solaire (parties électriques des capteurs solaires thermiques pour le chauffage ou l'eau chaude sanitaire…)"
    //             },
    //             {
    //               name: "Store électrique"
    //             },
    //             {
    //               name: "Sèche main et sèche serviette (si fixé au bâtiment)"
    //             },
    //             {
    //               name: "Sani broyeur"
    //             },
    //             {
    //               name: "Vidéophone"
    //             },
    //             {
    //               name: "Volet roulant motorisé"
    //             },
    //             {
    //               name: "VMC (Ventilation Mécanique Contrôlée pour la partie électrique)"
    //             }
    //           ]
    //         },        
    //       ]
    //     },
    //     {
    //       name: "Jardin",
    //       children: [
    //         {
    //           name: "Pompe d'arrosage automatique de jardin"
    //         },
    //         {
    //           name: "Pompe de forage et/ou relevage pour alimenter jardin"
    //         },
    //         {
    //           name: "Eclairage extérieur non solidaire aux bâtiments assurés"
    //         }
    //       ]
    //     },
    //     {
    //       name: "Piscine",
    //       children: [
    //         {
    //           name: "Pompe à chaleur pour piscine"
    //         },
    //         {
    //           name: "Pompe eau piscine"
    //         },
    //         {
    //           name: "Solaire piscine (panneaux, batteries, boîtier contrôle, etc…)"
    //         },
    //         {
    //           name: "Vannes motorisés"
    //         },
    //         {
    //           name: "Pompe de forage et/ou relevage pour alimenter piscine"
    //         }
    //       ]
    //     },
    //   ]
    // },
  ];


  var instance_tree = Tree.tree({
    children: $scope.typeBienTree
  });

  $scope.wrapper_tree = {
    tree: instance_tree,
    current_node: instance_tree,
    previous_node: null,
    level: 0,
  }

  function all_descendants(children){
    var list_all_descendants = [];
    var child;
    if(children.length == 0){
      return [];
    }else{
      for(index in children){
        child = {"name": children[index].name()};
        list_all_descendants = list_all_descendants.concat([child]);
        list_all_descendants = list_all_descendants.concat(all_descendants(children[index].children()));
      }
    }
    return list_all_descendants
  };

  function search_node(parent_node, item_name){
    var node = null;
    for(i in parent_node.children()){
      child_node = parent_node.children()[i];
      if(item_name == child_node.name()){
        return child_node;
      }else{
        node = search_node(child_node, item_name);
        if(node != null){
          break;
        }
      }
    }
    return node
  }

  function update_list(item_name, is_removed){

    var new_list = null;
    var descendants = null;
    var nodo = null;

    if(is_removed){

      // Busco el nodo
      nodo = $scope.wrapper_tree.current_node;

      // Actualizo historial
      $scope.wrapper_tree.level -= 1;

      if(nodo.name() == item_name){

        if($scope.wrapper_tree.level == 0){
          $scope.wrapper_tree.current_node = $scope.wrapper_tree.tree;
          $scope.wrapper_tree.previous_node = null;
        }else{
          $scope.wrapper_tree.current_node = $scope.wrapper_tree.previous_node;
          $scope.wrapper_tree.previous_node = $scope.wrapper_tree.current_node.parent();
        }

        new_list = all_descendants($scope.wrapper_tree.current_node.children());

      }else{

        if(nodo.parent().name() == item_name){
          $scope.wrapper_tree.previous_node = nodo.parent().parent();
        }

        new_list = all_descendants(nodo.children());

      }

    }else{
      // Busco el nodo
      nodo = search_node($scope.wrapper_tree.tree, item_name);

      // Actualizo historial
      $scope.wrapper_tree.previous_node = $scope.wrapper_tree.current_node;
      $scope.wrapper_tree.current_node = nodo;
      $scope.wrapper_tree.level += 1;

      if(nodo != null){
        // Busco todos los descendientes del nodo
        new_list = all_descendants(nodo.children());
      }
    }

    return new_list;
  }


  $scope.typeBien = all_descendants($scope.wrapper_tree.tree.children());

    
  // $scope.multimedia =[
  //     {"name":"Image et home cinéma"},
  //     {"name":"Audio et hifi"}
  // ];

  // $scope.gros =[
  //     {"name":"Lavage"},
  //     {"name":"Froid"},
  //     {"name":"Cuisson"}
  // ];

  // $scope.petits = 
  //   [{"name":"Cafetières/Machines à café"},
  //   {"name":"Grilles pain"},
  //   {"name":"Repassage"},
  //   {"name":"Aspirateurs"},
  //   {"name":"Coiffure"}];

  // $scope.infor = 
  //   [{"name":"Informatique"},
  //   {"name":"Téléphonie et tablette (Nomade)"},
  //   {"name":"Jeux vidéos"},
  //   {"name":"Photo et video"},
  //   {"name":"Lecteurs MP3 - multimédia"}];

  // $scope.inmobiliers = 
  //   [{"name":"Maison"}];
              

  $scope.marques = [];  
  $scope.models = [];
  var marqueName = null;
  function update_brand(name) {

    if (!($scope.marcas_modelos[name])){
      if ($scope.wrapper_tree.current_node.children().length == 0){
        $scope.id_categoria = $scope.categorias_con_ids[name];
        $scope.marques = Object.keys($scope.marcas_modelos[$scope.id_categoria]);
      } else {
        $scope.marques = [];
      }      

    }else{
      $scope.marques = Object.keys($scope.marcas_modelos[name]); //  ['LG', 'SAMSUNG']
    }
    
    // $scope.models = '';
    marqueName = name;
 

    // $scope.marcas_modelos_menu["marcas"] = $scope.marque;
    // $scope.marcas_modelos_menu["modelos"] = $scope.models;
  }


  $scope.update_model = function() {
    // $scope.marque = $scope.marqueSelected;
    if (!$scope.marcas_modelos[marqueName][$scope.marqueSelected]) {
      $scope.models = [];  
    } else {
      $scope.models = $scope.marcas_modelos[marqueName][$scope.marqueSelected];
    }
    
    
    // $scope.marcas_modelos_menu["modelos"] = models;
  };
  $scope.select_id_marque = function() {

    $scope.id_marca = $scope.marcas_con_ids[$scope.marqueSelected];
    
  };


  $scope.selectItemCallback = function(item){
    $scope.selectedItem = item;
    console.log($scope.selectedItem);
    $scope.typeBien = update_list(item.name, false);

    var selectedBien;

    $scope.showModele = true;
    
    if (item.name == "Téléviseurs") {
        selectedBien = 'TV_000';
    } else if (item.name == "Téléphonie mobile") {
        selectedBien = 'TLF_000';
    } else if (item.name == "Laptops") {
        selectedBien = 'COMPU_000';
    } else if (item.name == "Réfrigérateur standard" || 
        item.name == "Réfrigérateur compact" ||
        item.name == "Réfrigérateurs sans congélateur") { 
        selectedBien = 'FRIGO_000';    
    } else if (item.name == "Réfrigérateur américain" || 
        item.name == "Réfrigérateur congélateur en bas" || 
        item.name == "Réfrigérateur congélateur en haut" ||
        item.name == "Réfrigétateur combiné") {
        selectedBien = 'FRIGO_001';
    } else if (item.name == "Congélateur armoire" || 
        item.name == "Congélateur coffre" ||
        item.name == "Congélateur") {
        selectedBien = 'FRIGO_002';
    } else if (item.name == "Cave à vin service" || 
        item.name == "Cave à vin vieillissement" || 
        item.name == "Cave à vin multi-températures" || 
        item.name == "Cave à vin") {
        selectedBien = 'FRIGO_003';
    } else {
      selectedBien = item.name;
      $scope.showModele = false;
      $scope.showModele_gfk = true;
    }
    
    update_brand(selectedBien);
  };

           

  $scope.removeItemCallback = function(item){

    $scope.showModele = false;
    $scope.showModele_gfk = false;
    $scope.removedItem = item;
    $scope.typeBien = update_list(item.name, true);
    $scope.marqueSelected = '';
    $scope.modele = '';
    $scope.showFeatures = false;
    $scope.selectedItem = '';
    deactivateForms();
  };

  
  $scope.onSubmit = function () {
    console.log("submit");
    if($scope.multipleSelectForm.$invalid){
        if($scope.multipleSelectForm.$error.required != null){
            $scope.multipleSelectForm.$error.required.forEach(function(element){
                element.$setDirty();
            });
        }
        return null;
    }
    alert("valid field");
  };


           


  // ====================================  FEATURES LISTS ==============================================//
  // $scope.categorias_con_ids =  {"Multifonctions (MFD)": "c32001", "Plaques de Cuisson": "c32022", "Hottes": "c32026", "Appareils Photo Numériques": "c32310", "Cafetière et Expresso": "c32506", "Lave Vaisselle": "c32512", "Lave Linge": "c32516", "Sèche Linge": "c32519", "Radio/Radio-réveil": "c32521", "Réception satellite": "c32533", "Casques": "c32535", "Camescopes": "c32539", "Moniteurs": "c32547", "Lecteur DVD": "c32548", "Fer à Repasser": "c32553", "Robots": "c32557", "Aspirateurs": "c32561", "Cuisinière et Four": "c32562", "Desktops/Serveurs": "c32632", "Kits Oreillette": "c32643", "Disques Durs": "c32669", "Data/Video-Projecteurs": "c32683", "Enceintes PC / Stations MP3": "c32696", "Navigation Embarquée": "c32758", "Consoles de jeu": "c32798", "Baladeur Numérique (MP3/MP4)": "c321272", "Tablette": "c321373", "Mini Fours": "c329728", "Tireuse à Bière": "c329801"};

  //$scope.marcas_con_ids =   {"Acer": "90467", "hT-dsd":"sdfs", "ds sdf": "sdfs" };
  // $scope.marcas_con_ids = {"Acer": "90467", "Alcatel": "90562", "Bosch": "91077", "Brother": "91142", "BT": "96253", "Canon": "91215", "Citizen": "91336", "Crown": "310752", "Dell": "91568", "DeTeWe": "91588", "Develop": "91590", "Epson": "91904", "Fujitsu Siemens": "149582", "Gestetner": "92321", "Grundig": "92420", "HP": "92691", "IBM": "92736", "Infotec": "92790", "Jetfax": "92901", "Kodak": "93091", "Konica-Minolta": "309217", "KPN": "103353", "Kyocera": "93186", "Kyocera Mita": "232810", "Lanier": "93221", "Lexmark": "93281", "Medion": "93544", "Mita": "93661", "Muratec": "93761", "Nashuatec": "93785", "NEC": "93792", "OKI": "93932", "Olivetti": "93941", "Olympia": "93944", "Panasonic": "94065", "PANTUM": "677381", "Philips": "94157", "Pitney Bowes": "149387", "Plustek": "94210", "Rex Rotary": "94501", "Ricoh": "94514", "Sagem": "94665", "SAGEMCOM": "539257", "Samsung": "94679", "Sanyo": "94705", "Sharp": "94837", "Siemens": "94857", "Swisscom": "140861", "TA": "95208", "T-Com": "95291", "Toshiba": "95426", "Twen": "95498", "Utax": "95568", "Xerox": "95876", "1er Prix": "503352", "AEG": "90499", "Airforce": "115279", "Airlux": "218537", "Altus": "234872", "Amica": "90623", "Apelson": "226867", "ARCOOK": "1122043", "Ardo": "113280", "ARTHUR MARTIN": "667899", "Asko": "90737", "Atlantic": "96136", "Aya": "507910", "Balay": "90861", "Barazza": "495876", "Bauknecht": "90899", "Baumatic": "218529", "Beko": "90934", "Beldeko": "1229572", "Bluesky": "138917", "Bomann": "91067", "Bompani": "115354", "Bora": "231869", "Boretti": "270056", "Brandt": "115025", "Broan": "234525", "BSK": "218068", "California": "115027", "Candy": "91213", "Carma": "115029", "Carrefour Home": "432894", "Cata": "218556", "Climadiff": "218546", "Coldis": "227475", "Constructa": "91413", "Continental Edison": "138920", "Cook Art": "238595", "Cooke & Lewis": "596186", "Curtiss": "218071", "De Dietrich": "91540", "Delonghi": "218042", "Doman": "329659", "Domeos": "149294", "Domino": "231170", "Dynor": "218524", "Edesa": "115034", "Electrolux": "91833", "Electrolux-Arthur Martin": "218517", "Electrum": "542777", "Elegance": "91835", "Elica": "149110", "ENO": "91895", "Esco": "91925", "Essentiel B": "424208", "EVERTON": "664652", "Exceline": "524142", "Fagor": "92028", "FAR": "115039", "Faure": "218539", "Finlux": "113128", "Firstline": "115042", "Foster": "149111", "Franger": "226725", "Franke": "92181", "fratelli onofri": "328683", "Frecam": "231892", "Friac": "218514", "Frionor": "500813", "Fulgor": "92227", "Funix": "217937", "GAGGENAU": "92253", "GE": "92303", "Glem": "224229", "Godin": "218564", "Gorenje": "92381", "Grossbill": "338514", "Haier": "160430", "Harrow": "421954", "HDC": "563783", "HDC Link": "436543", "High One": "452474", "Homer": "480587", "Hoover": "92680", "Horn": "227486", "Hotpoint": "92687", "Hotpoint-Ariston": "90693", "Hudson": "227144", "Hyundai": "92728", "IAR": "115362", "Iberna": "92734", "Ignis": "92753", "Ikea": "292058", "IKEA": "625356", "Indesit": "92783", "Jeken": "231841", "Jemko": "238596", "Junker": "615123", "Juno-Electrolux": "92931", "King": "96966", "King D'Home": "293555", "KitchenAid": "93055", "Kneissel": "96976", "Koch": "93087", "Kontact": "149299", "Kueppersbusch": "93169", "Kunz": "93180", "Kupper": "421423", "Kuppersberg": "428519", "La Germania": "115367", "Laco": "93202", "Laden": "218543", "Lago": "225854", "Lazer": "139943", "Leonard": "279434", "Liebherr": "93290", "LIMIT": "1280288", "Link": "93311", "Linke": "452429", "Listo": "423164", "Luxhome": "559085", "Maison Valerie": "237630", "MANDINE": "1183737", "Markling": "218550", "MATTHIS": "689307", "Matthis Induction": "558312", "Midea": "264745", "Miele": "93630", "Mondial": "93698", "Mtec": "220088", "Nardi": "115371", "NEFF": "93796", "NEMAXX": "1080435", "Nodor": "231933", "Nogamatic": "218520", "NORD INOX": "682766", "Novidom": "338345", "Novy": "224163", "Oceanic": "93914", "Pelgrim": "268436", "Pitsos": "278205", "PKM": "94189", "Plus": "222501", "Presticook": "598829", "Privileg/Quelle": "94291", "Progress": "94321", "Proline": "94325", "Rommelsbacher": "94568", "Rosieres": "115376", "SAMANA": "811411", "Sancy": "115059", "Sauter": "218530", "Schaub-Lorenz": "94730", "Schneider": "116630", "Scholtes": "94760", "Scientific Labs": "545547", "Selecline": "218054", "Selection": "142564", "Sidex": "218547", "Signature": "298210", "Siltal": "94876", "Smalvic": "218553", "Smeg": "94927", "Sogelux": "222504", "Spider": "139564", "Star": "95059", "Steba": "95084", "Stoves": "222890", "Teba": "222894", "Technical": "226063", "Techwood": "274619", "Techyo": "452749", "Tecnolec": "224234", "Tecnolux": "307784", "Teka": "95277", "Telefunken": "95286", "Terim": "225115", "Thermor": "113292", "Thomson": "95367", "Triomph": "217953", "Unic Line": "149306", "Urania": "95563", "Valberg": "452475", "VENTE PRIVEE": "1126698", "Vestel": "95620", "VIESTA": "1123211", "Viva (Bsh)": "426607", "V-Zug": "235812", "Waltham": "149195", "Wells": "218531", "Weltco": "232256", "Westline": "329097", "Whirlpool": "95787", "White And Brown": "217940", "WMA": "825936", "Zanussi": "95902", "Zerowatt": "115079", "Airone": "271886", "Akpo": "293579", "Alizee": "419885", "Allegro": "90579", "Alno": "90593", "Amsta": "218538", "Appliance": "314713", "Aspes": "115022", "Autogyre": "457814", "Axess": "90831", "Axiair": "439482", "B. Epoque": "218565", "BAUMATIC UK": "1105906", "Bell": "232811", "Belling": "222216", "Berbel": "326086", "Bertazzoni": "510686", "Best": "90971", "BODNER & Mann": "296018", "Brandy Best": "435640", "Bricorama": "237152", "Castorama": "237141", "Corradi": "272810", "Cuisinella": "218560", "Curling": "218527", "Cylinda": "274895", "Designair": "482796", "Devel": "286417", "Dmo": "307105", "Domair": "268521", "Dometic": "316761", "Domo": "113701", "Ecg": "271356", "EDY": "268432", "Eico": "96501", "Ekoline": "454369", "Elcolux": "224701", "Elitair": "417801", "Eternal": "223559", "Etis": "316840", "Eureka": "226790", "Eurodomo": "96571", "Faber": "234840", "Fadis": "415771", "Falco": "1066266", "Falcon": "219520", "Falmec": "271884", "FOX": "92174", "Francia": "218525", "Gutmann": "92448", "HBH": "218544", "Helkina": "218062", "Hygena": "218551", "Ices": "224745", "Igenix": "295843", "Ilve": "225106", "Innova": "92797", "Inter Gorenje": "218522", "Jet Air": "267103", "Klarstein": "568729", "Lacanche": "293413", "Ladywind": "218548", "Leisure": "218541", "Luxor": "93382", "Matfor": "218558", "Maya": "399854", "Mepamsa": "226887", "Metal": "97150", "Microligh": "218552", "Mobalpa": "218536", "Modulair": "218566", "New Air": "260305", "Oranier": "93992", "Pando": "231939", "Portinox": "583176", "Premiere": "94269", "Prima": "97391", "Rangemaster": "292281", "Recco": "320124", "Rectiligne": "218523", "Respekta": "94491", "Robin": "227933", "Roblin": "271377", "Sagoma": "1171503", "Samac": "218519", "Samba": "218540", "Schmidt": "594249", "Sideme": "227489", "Silverline": "97630", "Technoline": "285365", "Technolux": "285366", "Tecnogas": "149112", "Tecnowind": "218518", "Tekma": "224702", "Tekno": "493636", "Tonda": "218562", "Turbo": "95489", "Turboair": "264890", "Unelvent": "224703", "URBAN": "1050356", "Venmar": "422111", "Ventolux": "439268", "Victory": "218557", "Viva": "487523", "Vortice": "223801", "White Westinghouse": "115077", "Wild": "218528", "Windsor": "218526", "Zirtal": "510771", "4World": "419382", "Acorn": "103526", "Advent": "217794", "Agfa": "90509", "Agfaphoto": "432063", "Aigo": "307370", "Aiptek": "220385", "Airis": "139410", "Aito": "290787", "Akor": "233189", "Amstrad": "90629", "Aosta": "296594", "Apple": "90660", "Archos": "223684", "Argus": "225223", "Atipix": "309155", "Atlantis-Land": "338735", "AUTOGRAPHER": "1107598", "Avant": "113120", "Benq": "281610", "Bluetech": "427734", "Braun Germany": "367591", "Bravus": "515883", "Bresser": "225229", "BRINNO": "659134", "BTC": "91157", "Bushnell": "225233", "CAMSPORTS": "668910", "Canal Toy's": "229493", "Carrefour": "103762", "Casa": "247862", "Casio": "91254", "CCam": "288765", "CEL-TEC": "688249", "Che-Ez": "288813", "Chinon": "91322", "Clipsonic": "233182", "Cobra": "91359", "Conceptronic": "261103", "Concord": "91401", "Connectix": "96347", "Contax": "142715", "Cool-Icam": "287627", "CORDEX": "1099123", "Crayola": "142760", "Creative": "91467", "CYBER EXPRESS ELECTRONICS": "1230870", "Cyberhome": "142341", "Darling": "296582", "Denver": "96419", "Digimaster": "314657", "Digital & Perspective": "368376", "Digital Blue": "326103", "Digital Concepts": "317771", "Digital Dream": "222143", "Digitrex": "288933", "Disney": "316789", "DNT": "91645", "Doerr": "142865", "Dxg": "316382", "DXO": "417765", "Easypix": "431064", "Eden": "140283", "Emprex": "305835", "Energy Sistem": "292661", "Ergo": "91910", "Exakta": "91995", "Ferrania": "227506", "Fisher-Price": "92109", "Fujifilm": "219523", "Fuuvi": "609119", "Gelcom": "293570", "Genius": "92308", "Giochi Preziosi": "583437", "Gopro": "443672", "Hasbro": "287802", "Hasselblad": "92543", "Hello Kitty": "287369", "Hercules": "273109", "Hitachi": "92644", "Hunter": "225250", "Imc": "223635", "Ingo": "443599", "Inovalley": "315380", "Instar": "574724", "Intel®": "96880", "Intova": "513268", "ION": "814978", "It Works": "265550", "I-Think": "315753", "IZYTRONIC": "1171380", "Jaga": "305976", "Jay-Tech": "291037", "Jenoptik": "96919", "JVC": "92937", "Keystone": "93032", "KIDZ CAM": "699881", "Kobishi": "284722", "Kocom": "274588", "Koenig": "93093", "Konica": "93110", "KRIONIX": "740037", "Krypton": "290564", "Labtec": "220087", "Leica": "93253", "Lenco": "93263", "Lexibook": "93279", "Little Tikes": "434660", "LKM": "1196538", "Logitech": "93335", "LTL ACORN": "1099125", "Lumicron": "326271", "Luxya": "455541", "LYTRO": "749693", "Maginon": "93419", "Magpix": "290440", "MAPTAQ": "671261", "Mattel": "218225", "Maxell": "93507", "Mecer": "324155", "Media-Tech": "287231", "Mercury": "93582", "Minolta": "93651", "Minox": "93652", "Mistral": "93660", "MONSTER HIGH": "668914", "MPman": "145113", "Mustek": "93764", "Mystral": "325127", "NARRATIVE": "1119809", "Nashita": "227510", "NCTECH": "1128335", "Neo": "317790", "Neom": "327695", "Neoxeo": "315632", "Nexicam": "305603", "NGS": "150356", "Nikon": "93838", "NK": "563938", "Nomatica": "295819", "Nortek": "113522", "Novadia": "293710", "Novatek": "288814", "Odys": "329933", "Olympus": "93946", "Omisys": "315629", "Oregon Scientific": "230811", "OUAPS": "1095465", "OVERLOOK": "725425", "Packard Bell": "94049", "Palm": "224507", "Peekton": "310851", "Pen Drive": "292093", "Pentagram": "306512", "Pentax": "94122", "PhaseOne": "421599", "PIVOTHEAD": "829795", "Pixturize": "1206334", "Plawa": "220245", "Playskool": "139950", "Pnj": "438204", "Polaroid": "94222", "POWERSHOVEL": "713159", "Praktica": "94259", "Premier": "94268", "Pretec": "227653", "Prolink": "265406", "Pxor": "601856", "Pyle": "94359", "QPS": "221168", "Q-Ware": "231294", "Reflecta": "94449", "Reflex": "94450", "Relisys": "94478", "Rik & Rok": "237158", "Rimax": "218491", "Rollei": "94562", "Sakar": "218137", "Sampo": "94677", "Sangha": "295809", "Sanrio": "400862", "Scott": "94792", "Sealife": "97585", "Shiro": "301503", "Sigma": "294062", "Sigmatek": "308878", "Silverlit": "420182", "Sipix": "272969", "Skanhex": "288419", "Smart": "94923", "Smoby": "418827", "Sony": "94978", "Soundstar": "396271", "Soundwave": "94987", "Speedo": "115897", "Spin Master": "583476", "Spypoint": "743626", "Starblitz": "95064", "Stealth": "272116", "SUPERHEADZ": "527890", "Swann": "222892", "Sweex": "290179", "SWIMMING FLY SO": "673450", "Targa": "95234", "Tasco": "95238", "Techmobility": "317770", "Technaxx": "339138", "TECHTRAINING": "733866", "Teknofun": "599259", "Terratec": "97786", "Thompson": "147003", "Thumbs Up": "231338", "T'NB": "103756", "Tokiwa": "218061", "Trevi": "95451", "Trust": "95472", "Typhoon": "141061", "U": "222631", "Ultrasport": "600032", "Umax": "95529", "UNOTEC": "726222", "VD-Tech": "419608", "Vea": "305685", "VEO": "296583", "Verbatim": "95611", "Videojet": "625261", "Vista Quest": "455761", "Vitech": "273743", "Vivitar": "95672", "Vtech": "95697", "Waitec": "115887", "Werlisa": "217934", "Worldsat": "219050", "Yakumo": "95881", "Yamada": "290643", "Yashica": "95887", "YONIS": "1055825", "Yoo Digital": "511539", "Yukai": "272541", "zstar": "749467", "ABC": "90443", "AC-HOME": "802571", "Acm": "295990", "ACOPINO": "712619", "Addex": "221489", "Adler": "90490", "ADNAUTO": "1161469", "AFK": "90505", "Aitek": "326305", "AKA": "90535", "Akiba": "218075", "Alessi": "90565", "Alfa": "90567", "ALINEA": "611374", "All Ride": "218180", "Altilux": "279540", "Amadis": "218095", "Amazon Basics": "545267", "Ariete": "90688", "Aroma": "218100", "Arzum": "290414", "Ascaso": "417861", "Astoria": "218047", "Auchan": "142347", "Avilla": "455550", "Barista": "1160240", "Bartscher": "285494", "Beem": "90923", "Bella Professional": "571146", "Bellux": "271501", "Belmio": "1207821", "BELMOCA": "830091", "Beper": "493724", "Bestron": "96201", "Betron": "218049", "Bialetti": "218079", "Bien Vu": "338744", "BLACK PEAR": "707963", "Black&Decker": "91020", "Blaupunkt": "91023", "Bluebell": "493638", "Bob Home": "317537", "Bodum": "91051", "BONAMAT": "665302", "Braun": "91095", "Breville": "218511", "Briel": "218081", "Brothers Choice": "298187", "Bugatti": "261877", "Butler": "142507", "C3": "324412", "Cads": "218078", "Caf": "305430", "Calor": "218094", "Camry": "91211", "Carpoint": "427871", "Carrefour Discount": "611365", "Casino": "218484", "Caso": "435860", "CASSELIN": "1096105", "Chefn": "599507", "CHEMEX": "1197746", "Chromex": "217948", "Cilio": "115090", "Cimbali": "259428", "Clatronic": "91346", "Cleveland": "233117", "Cloer": "91352", "Coffee Boy": "218089", "Coffee Cream": "314380", "Coffee Maxx": "438817", "Comi": "218096", "Conrad": "91411", "Convivium": "601453", "COSYLIFE": "677571", "CREMESSO": "527201", "Crena": "482683", "Crousti Light": "508641", "Cuisinart": "339933", "Cuisinier": "303300", "Cuisitech": "499438", "Cyclone": "287168", "Daewoo": "91506", "Dellar": "423369", "Delta Q": "454268", "Denwa": "326697", "DIDIESSE": "724989", "Domedia": "565959", "Domena": "91661", "Domoclip": "326908", "Drink Maxx": "435373", "D-tech": "459138", "Dualit": "143670", "Dyras": "98538", "E.ZICOM": "865313", "ECM": "274106", "Eco+": "264582", "ECODE": "1067596", "Ecron": "138924", "Eculina": "1210321", "Efbe-Schott": "94764", "Elcotec": "218093", "Electric Co.": "264973", "Electronia": "109061", "Elektra / Tradebrand Kruidvat": "403288", "Elsay": "142553", "Elta": "91861", "Emerio": "599643", "Emide": "91875", "Entronic": "231639", "Europa Style": "91972", "Eurotech": "91979", "Evatronic": "459482", "Everglades": "231656", "Exido": "291409", "Faema": "92025", "Fakir": "92031", "Figui": "218044", "First Austria": "271366", "Form+Funktion": "92163", "FrancisFrancis!": "160431", "Frifri": "230435", "G3Ferrari": "1051206", "Gaggia": "92254", "Gastroback": "92276", "GAT": "868358", "Girmi": "92345", "Glenan": "218059", "Gotech": "431101", "Gourmet Maxx": "573377", "GPS ROUTE": "1182784", "Graef": "92391", "GRAFNER": "1121177", "Grossag": "92414", "Guzzini": "92450", "H.KOENIG": "625927", "HABITEX": "687487", "Hamilton Beach": "92499", "Handpresso": "1027840", "Harper": "223303", "Hema": "221413", "Heru": "92605", "HOBERG": "1085418", "Homday": "481433", "Hometech": "232252", "Ideeo": "323858", "Illy": "233007", "Inventum": "92834", "ITT": "92860", "J&R": "324545", "Jata": "115045", "JETTECH": "521529", "Jocca": "323657", "Jura": "92933", "Kaisui": "142750", "Kalije": "419918", "Kalorik": "92967", "Karcher": "92982", "KEM": "231813", "Kenwood": "139332", "K-Fee": "548588", "Kiovea": "524720", "Kitchen Chef": "436241", "Koala": "233323", "KOENIG": "626792", "Kooper": "523013", "Korona": "93120", "Krea": "1143726", "Krups": "93157", "La Cimbali": "226795", "La Pavoni": "93197", "La Piccola": "426132", "Lacor": "273815", "Lagrange": "218067", "Laguiole": "262551", "Lamarque": "309027", "Lampa": "456006", "Lavazza": "218087", "Legal": "559029", "LELIT": "665208", "Lentz": "416439", "Leysieffer Kaffee": "1163073", "Ligne Chrome": "290993", "Liventa": "430909", "LUCAFFE": "1130585", "Lulu Castagnette": "426382", "Lysitea": "478454", "Maestro": "917063", "Magefesa": "232353", "Magimix": "217936", "Makita": "93437", "Malongo": "230713", "MANTA": "1120804", "Martello": "496130", "Matea": "548120", "Max Italia": "292202", "Md": "301863", "Melitta": "93566", "Menage": "403172", "Mesko": "274563", "MIA": "93607", "Micromax": "218045", "Midland": "223028", "MINI MOKA": "853503", "MNI": "1203038", "Moka": "222747", "Monix": "231930", "Morphy Richards": "93716", "Morris": "113289", "Moulinex": "93730", "M-Tec": "217730", "Mulex": "442214", "Mx Onda": "140856", "Myria": "436852", "Naelia": "459972", "Nemox": "261982", "Nescafe": "423764", "Nespresso": "218053", "Nesta": "396339", "Nestle": "93899", "Neufunk": "270389", "Nevir": "139946", "New Pol": "112463", "Nivona": "367176", "NORDIC HOME CULTURE": "1196196", "Nova": "93883", "Nuova Simonelli": "287368", "Obh Nordica": "293600", "Orbegozo": "231937", "Orima": "267205", "Orva": "217941", "Oster": "94021", "OURSSON": "728122", "Palson": "139949", "Pavoni": "218090", "Peak": "453094", "PEM": "1211629", "Petra": "94141", "Polti": "94231", "Powertec Kitchen": "625458", "Prim'Truck": "1229521", "Princess": "94285", "Prinston": "138901", "PROFICOOK": "687241", "QBO": "1207337", "QILIVE": "1026401", "Quigg": "606761", "Rancilio": "226799", "Raydan": "415643", "Revelys": "291000", "Ritter": "94532", "Riviera": "218097", "Riviera & Bar": "226800", "Roadstar": "94539", "Robusta": "431129", "Rombouts": "285627", "Romix": "280993", "Rowenta": "94600", "RUN": "218050", "Russell Hobbs": "94632", "Saba": "94646", "Saeco": "94657", "Salco": "94669", "Salton": "94674", "Sapir": "322238", "Saro": "221454", "Scarlett": "290573", "Seaway": "145134", "SEB": "218040", "Segafredo": "423914", "Sencor": "223225", "Sensio": "441271", "SENYA": "1157235", "Servitech": "218099", "Severin": "94833", "Silver Style": "314356", "SilverCrest": "424128", "Simac": "94883", "Simeo": "310408", "SIMPLY": "659363", "Sinbo": "290430", "Singer": "94895", "Siplec": "218051", "SMARTER": "1088262", "Sogo": "138905", "Solac": "94961", "Solis": "94965", "Spd`Line": "322638", "Spidem": "217949", "Starway": "226904", "Suntec": "139566", "SUNTEC WELLNESS": "905154", "Support Plus": "233979", "Swan": "297737", "Swisstech": "218088", "Symex": "306020", "Taurens": "218074", "Taurus": "295813", "Tchibo": "97766", "Teacof": "433115", "Team": "95248", "Technivorm": "142517", "Techno": "327184", "Techno Diffusion": "218086", "Techno Sangoo": "340225", "Technomax": "273423", "Technostar": "285178", "TEESA": "1140919", "Tefal": "95272", "Termozeta": "218436", "THE KITCHENETTE": "1167019", "TM Electron": "417849", "Top Budget": "428336", "TOP CHEF": "1060205", "Tous Les Jours": "610263", "Tower": "223495", "Trendy": "323198", "Trion": "310790", "Trisa": "95464", "Tristar": "95465", "Turmix": "223616", "TV DAS ORIGINAL": "698915", "Ufesa": "218046", "ULTRATEC": "1082965", "Unold": "95556", "VENGA": "674480", "Vibell": "231618", "Viceversa": "227019", "Villaware": "438563", "Virages": "218091", "Viscio Trading": "1207499", "Waeco": "95706", "Waves": "441460", "Wellness & Care": "1150695", "Westwood": "95781", "WIK": "95801", "Wilden": "95806", "Winkel": "544588", "Winny": "419750", "WMF": "284704", "Zelmer": "95915", "Zephir": "224243", "Zomix": "295807", "Airport": "222489", "Apell": "222493", "Aquaceane": "222491", "Ardem": "138915", "Artic": "115021", "Blomberg": "91032", "Bravo": "222496", "Carad": "115028", "Clayton": "269536", "Climaspace": "572246", "Edson": "501961", "Exquisit": "92004", "Favorit": "92048", "Frigistar": "298365", "Galanz": "238605", "HEC": "92562", "INEXIVE": "1182088", "Jpc": "285914", "LG": "93284", "Linetech": "419919", "Manhattan": "93449", "Maytag": "115050", "Minea": "238559", "Ocean": "93912", "ORIGANE OLF": "877076", "Ormond": "293283", "OXFORD": "1108253", "Radiola": "138902", "Schauen": "428540", "SE Electronic": "513155", "Servis": "222217", "Surfline": "310224", "Tucson": "457818", "Vedette": "218545", "Wellton": "431742", "Wesder": "237884", "Whitewash": "418239", "Witewash": "396266", "Xper": "115383", "Alaska": "90553", "Altic": "227473", "Aristo": "321642", "Asterie": "227481", "Ava": "397024", "Axane": "222494", "Bellavita": "452746", "Bendix": "90944", "Bluewind": "227472", "Boreal": "115355", "Calex": "96274", "Comfee": "544837", "Dawlance": "328630", "Deawoo": "397751", "Dyson": "91751", "Elvita": "113285", "Eudora": "91946", "Eumenia": "91950", "Faraon": "227477", "Frigidaire": "112464", "Galant": "262081", "Hemmermann": "115043", "Hightec": "512746", "Hisense": "282581", "Hohl": "227490", "JPC": "1024988", "Kenmore": "226726", "La Redoute": "219232", "Lindbergh": "444346", "Master Chef": "443387", "Mastercook": "313997", "MEA": "247911", "MUBARIK": "1166722", "ONECONCEPT": "1036846", "Otsein-Hoover": "115055", "Perfekt": "94130", "Philco": "94156", "Polar": "94220", "Record": "94441", "Renlig": "433850", "San Giorgio": "94684", "Sedif": "222502", "SEG": "94803", "Siera": "314921", "Vendome": "227474", "VON HOTPOINT": "1102631", "Wellington": "310157", "Arctic": "90678", "Atlus": "273281", "Creda": "96374", "DANUBE": "1114777", "Falda": "271496", "GENERISS": "810490", "Ipso": "140871", "Kerwave": "276642", "Konrad": "115364", "LACASA": "1068382", "MERKER": "1096129", "Thomas": "95364", "White Knight": "97993", "3Go": "508696", "Acctim": "310769", "ADIN": "683990", "Agashi": "113099", "Aiwa": "90534", "Akai": "90538", "Akira": "290355", "Akura": "90547", "Alba": "90554", "Albrecht": "90560", "Altec Lansing": "96076", "Amethyst": "455691", "Arelec": "232839", "Art Sound": "290252", "Artech": "139929", "Astone": "316997", "ATYLIA": "856406", "Audio Box": "396990", "Audio Pro": "227311", "AudioAffairs": "841165", "AUDIOCORE": "696452", "Audiola": "217957", "Audiopole": "432739", "Audiosonic": "90783", "August": "436231", "Auna": "487909", "AVENGERS": "906381", "AVENZO": "812945", "aves": "810893", "Avox": "420187", "Awa": "231129", "Axion": "90833", "Axxion": "271806", "B & O": "103347", "Balance": "366408", "Barbie": "219509", "Basicxl": "575012", "Batman": "397109", "BAYAN AUDIO": "686589", "Be": "267453", "BE MIX": "1127097", "Bernstein": "233978", "BIG W": "732597", "BigBen Interactive": "270788", "Biostek": "317983", "BLACK PANTHER C": "856365", "Blow": "501985", "Bluestork": "433138", "Bml": "91045", "Boombox": "260387", "Boomstar": "1225226", "Boost": "260281", "Bose": "91079", "Boston Acoustics": "96238", "Brionvega": "91132", "Brondi": "103832", "BTS": "91158", "Bush": "91185", "Caliber": "96275", "Cambridge Audio": "324342", "Casung": "314777", "Centurion": "96295", "CGV": "259483", "Clint": "527133", "CMP": "217812", "CMX": "423026", "Coby": "139931", "Com-One": "237184", "Connect Research": "512157", "Cotech": "221037", "Cresta": "91471", "Crony": "260647", "Crosley": "115356", "Crystal": "96378", "Cube": "339227", "CURVE": "694731", "Cygnett": "416956", "Day-Break": "504269", "Dcybel": "1130775", "Delcom": "139934", "Denca": "264408", "Denko": "218844", "Denon": "91578", "Derens": "237883", "Dewalt": "91542", "DEXFORD": "692927", "Dieci": "142752", "DIGIVOLT": "666628", "DISUN": "806707", "DITALIO": "1084600", "Divoom": "436780", "DJ-BOX": "836312", "D-Jix": "419844", "drobak": "805105", "Dual": "91708", "Durabrand": "270695", "DURONIC": "906706", "Dust": "499231", "DYNABASS": "896808", "Dynavox": "420645", "Dyon": "509466", "Ea2": "815352", "Easy Touch": "316790", "Edenwood": "543845", "Edifier": "327828", "Ednet": "261829", "Einhell": "91804", "EKIDS": "1099974", "Elbe": "91822", "ELECITI": "1265465", "Eltax": "91863", "Eltra": "91864", "Emerson": "91873", "Engel": "223460", "Engel Axil": "674833", "Epok": "516126", "Esperanza": "274542", "Eton": "96563", "Etsuko": "232840", "Eurocom": "103728", "Europsonic": "142566", "Evergold": "232842", "Evidence": "317667", "ezGear": "420239", "Fenner": "92068", "Ferguson": "149191", "FINESOUND": "1254977", "FIVESTAR": "1125561", "Flint": "149295", "FM": "226741", "Forever": "293427", "FPE": "453425", "Freecom": "232346", "Freeplay": "222817", "Fresh L.": "96668", "Fusion": "221347", "Fuxinko": "1203836", "Gear4": "420146", "Geepas": "323783", "Gemex": "92301", "Gemini": "103522", "Geneva": "445416", "Global Sphere": "270769", "Goclever": "453026", "GOLD STAR": "1140062", "Goldstar": "92373", "Goodmans": "92380", "GPO": "443588", "Grandin": "138928", "Griffin": "231380", "Gulli": "1181774", "H&B": "273819", "Hama": "92497", "Hannspree": "368278", "Hardel": "445103", "Hdigit": "511449", "Heden": "396267", "Hisawa": "149297", "HOE": "1173915", "Hoher": "267558", "Homedics": "272147", "Homemix": "273280", "HQ": "115890", "HT": "514498", "Hypson": "142560", "IBIZA SOUND": "1166633", "I-CAPTURE": "500775", "Iconbit": "600120", "Icy Box": "329852", "IDANCE": "744744", "IDT": "220378", "Ifun": "427647", "iHome": "324025", "I-JOY": "443856", "Ilive": "482798", "Iluv": "437504", "Imagina": "307448", "Imperial": "92771", "INKI": "697617", "Inovaxion": "416638", "Intempo": "305986", "Intenso": "219755", "International": "92817", "Intersound": "92823", "I-Random": "419852", "IRC": "521600", "Irox": "455092", "Irradio": "113507", "IRT": "319070", "Jamo": "92880", "JBL": "92887", "Karma": "213876", "Kasuga": "92993", "KENGTECH": "1236041", "Kenwin": "422455", "Kerzo": "270006", "Khorus": "290510", "Kitsound": "493757", "Klervox": "149564", "Kooky": "278989", "KOOL.STAR": "1262183", "KRUGER & MATZ": "687616", "Kwai": "218843", "kwmobile": "989597", "Lacrosse Technology": "317778", "LAMAX": "1105965", "Lansay": "142555", "Lasonic": "269934", "Lauson": "139942", "Leclerc": "236342", "Lecsound": "218853", "LEGAMI": "743741", "Lego": "227166", "Leotec": "320455", "LeSenz": "1155899", "Lexon": "93282", "Lextronix": "428994", "Lloytron": "149901", "Logic 3": "97064", "Logik": "428858", "Logilink": "441309", "Lotronic": "544399", "lovemytime": "482243", "Lowry": "545264", "Ltc": "306487", "Macally": "116318", "Madcow": "320594", "Madison": "93406", "Magic Box": "228312", "Magnum": "93423", "Majestic": "145032", "Manesth": "142754", "Manta": "285094", "MAQ": "572193", "Mark": "113130", "Marquant": "116593", "Mate Star": "232559", "Matsui": "218009", "MAWASHI": "872893", "mayhem": "329877", "MBC": "142556", "Memorex": "93569", "Metabo": "93592", "Metronic": "103761", "Microlab": "326662", "Milwaukee": "93641", "Mitsai": "140309", "Mobility Lab": "597745", "Monitor Audio": "220534", "Monoprix": "261625", "Monster": "327295", "Motorola": "93726", "Moxie": "618946", "MR.WONDERFUL": "1029087", "Msonic": "323221", "MTK": "457092", "Muse": "224476", "MUSKY": "848015", "Muvid": "429504", "MY DEEJAY": "1191876", "Naf Naf": "218846", "Naiko": "142571", "Nanda Home": "611375", "National Geographic": "293169", "NES": "293099", "Nesx": "309055", "New One": "457586", "Nikkei": "113521", "Nilox": "428332", "NIZHI": "801835", "Nostalgic": "222858", "Novis": "268558", "Noxon": "525147", "Odeon": "232849", "Okano": "93930", "Omega": "93948", "ON.EARZ": "1036882", "Ondex": "142552", "ONE by SEG": "756130", "ONE PLUS": "753707", "Onn": "435813", "Optimag": "292871", "Orion": "94001", "Orium": "323805", "Oshiwa": "142751", "Oxx": "504111", "OXX Digital": "454231", "Oxygen": "94035", "Ozaki": "235649", "Pacific": "94048", "Paris Saint-Ger": "852792", "Parrot": "290621", "Party Light&Sound": "1229354", "Peha": "94112", "PERFECTPRO": "836375", "Philips Nike": "314688", "Pinell": "612850", "Pioneer": "94180", "PLATYNE": "1257643", "Plustron": "218158", "Pointer": "148851", "Pollyflame": "115338", "Pop": "231724", "POSS": "1087526", "POWERplus": "989615", "Prestige": "94274", "Prestigio": "310107", "Pro Basic": "139951", "Professor": "271360", "Profitec": "97401", "PROLINE AR": "1255190", "PROSMART": "1201643", "Prostar": "142559", "PRUNUS": "1262228", "psyc": "1034504", "Pure": "287626", "Pure Acoustics": "495988", "Q2": "506846", "QOOPRO": "686010", "QUBE": "1193555", "Quer": "459185", "R.O.GNT": "812658", "Radialva": "142554", "Radiotone": "94391", "Reflexion": "329726", "Renkforce": "422809", "Revo": "262563", "Ricatech": "427503", "Ricco": "458719", "Roberts": "218022", "Rowa": "225574", "Rueducommerce": "339367", "Ryobi": "94637", "S&D": "431299", "S.DIGITAL": "697615", "S2 Digital": "426911", "Sailor": "230076", "Saisonic": "400809", "Salora": "94673", "Sangean": "97534", "Sansui": "94700", "SARDINE": "1150063", "Satzuma": "519408", "Scansonic": "113134", "Schneider/TCL": "94755", "Schwaiger": "94779", "SDI": "227949", "SDIGITAL": "1124893", "Sedea": "219080", "Shark": "97610", "Silva Schneider": "113534", "Skymaster": "94917", "Skytec": "287394", "Socrimex": "232847", "Sonoro": "431199", "SOULRA": "736236", "Sound Tech": "366900", "SOUND2GO": "810525", "Soundfreaq": "606733", "Soundmaster": "94986", "Soundmax": "235667", "SPC Telecom": "291953", "Spiderman": "437907", "Spirit": "101752", "Spirit of St. Louis": "231953", "Stanley": "217658", "Star Wars": "278609", "Steepletone": "220382", "Steljes Audio": "1211636", "STEREOBOOMM": "854848", "Storex": "279502", "Strong": "95130", "Subsonic": "418155", "Sunfield": "327887", "Sunkai": "145132", "Sunstech": "307123", "Supertech": "95169", "Supra": "421825", "Sytech": "305128", "Tacens": "447972", "Takara": "142756", "Tamashi": "95223", "Tangent": "220558", "Target": "95235", "TCM": "274109", "TDK": "95246", "Teac": "95247", "TECHLY": "731529", "Technisat": "95258", "Tecsun": "401446", "Ted Baker": "324745", "Telemax": "258069", "Telestar": "97782", "Tellur": "743813", "Tensai": "95318", "Teufel": "95337", "TFA": "95345", "THALASSA": "710931", "Tivoli": "227583", "Tivoli Audio": "310840", "TIWIGI": "1202583", "Tokai": "97812", "Toolland": "298213", "Tunbow": "527333", "United": "95547", "Vakoss": "323219", "Venturer": "97924", "Vibe": "263003", "Vibe-Tribe": "1057211", "Vieta": "233969", "Viewquest": "366961", "Vita Audio": "434795", "VOV": "422801", "VQ": "1202035", "VTIN": "1179519", "VXR": "1264536", "Walkvision": "232417", "Watson": "95733", "We": "452326", "Witti": "1154738", "Woxter": "270173", "X4-Tech": "307856", "X-mini": "504461", "Xoro": "282892", "Xtreme": "314987", "Xtrememac": "338987", "Yamaha": "95882", "Yoko": "95891", "Yorx": "95894", "Zipy": "318266", "Zoetac": "686671", "1 Z": "90422", "Ab": "328505", "Absat": "219053", "ADB": "140585", "ADT": "271900", "Alcad": "573540", "Aldes": "219060", "Allsat": "219063", "Allvision": "290187", "Alma": "566814", "Amiko": "589253", "Amitronica": "288668", "AMTC": "482716", "Anttron": "572204", "APM": "265496", "Artec": "90716", "Aston": "219073", "Astrell": "302153", "Asus": "90752", "ATEMIO": "689900", "Atevio": "564139", "Atlanta": "90766", "ATLAS": "1144093", "Atsky": "295905", "Aurex": "421826", "Auvisio": "340050", "Avanit": "525725", "Avermedia": "317085", "Axas": "574453", "Axil": "230176", "Axitronic": "421457", "Azbox": "530415", "Balmet": "419623", "Belson": "221175", "BEST BUY": "150352", "Bigsat": "420228", "BXL": "1175600", "Cablecom": "419375", "CABLETECH": "670262", "CAHORS": "867243", "Canal Digital": "322784", "Canal Plus": "219043", "Canal Satelite": "219042", "Captimax": "1179393", "Cherokee": "419894", "Chili": "292037", "CityCom": "91339", "CM3": "674644", "Colombus": "219093", "Columbia": "271626", "Columbus": "219082", "Comag": "228267", "Cosat": "219088", "Cristor": "459973", "CRT": "749359", "Cubsat": "273179", "CYBEST": "740265", "D2 Diffusion": "220083", "Dak": "427787", "Devolo": "234500", "Digiality": "291075", "Digihome": "273056", "Digilogic": "338800", "Digiquest": "259504", "Digitalbox": "472919", "Digitek": "149374", "Digitronic": "284691", "Disch": "219054", "Discovery": "91631", "Distra": "219061", "Distratel": "338963", "Distribat": "219055", "Distrisat": "219076", "Division": "272803", "Dream": "224560", "Dreambox": "431308", "Dse": "366594", "DTSAT": "1124793", "Dune": "219065", "Dvico": "290824", "Easy One": "508486", "ECHOSAT": "1277817", "Echostar": "96487", "Edision": "419982", "Elanvision": "418585", "Elap": "219064", "Emme Esse": "116398", "Emos": "368276", "Emtec": "149258", "E-Tek": "403105", "Eurielt/Dist": "219049", "Europhon": "91974", "Europsat": "293242", "Evology": "437739", "Evolve": "200080", "Eycos": "415757", "F.P.E.": "440079", "FetchTV": "523477", "FMD": "103775", "Fonestar": "140305", "Formenti": "219059", "Formuler": "1189364", "Fortecstar": "325789", "Fracarro": "116400", "Fransat": "549966", "Freesat": "447893", "FTE": "92213", "Fuba": "92215", "Fuji Magnetics": "92220", "Fuji Onkyo": "290020", "Galaxis": "92256", "Gibertini": "225175", "GIGA BLUE": "696047", "GIGA TV": "722483", "GLOBO": "1097877", "GLOBSAT": "658891", "Golden Interstar": "340396", "Golden Media": "563862", "Goobay": "403290", "Gosat": "521396", "Green Technology": "290321", "Hauppauge": "109107", "Hb": "92554", "HD LINE": "1105927", "Hiremco": "1166256", "Hirschmann": "92640", "Hiteker": "271944", "Homecast": "323789", "Humax": "96840", "I-Can": "304998", "Iisonic": "304737", "Ikusi": "398943", "Imex": "219087", "INOUTTV": "659332", "Intervision": "92827", "Intex": "92828", "Intuix": "307902", "Inverto": "393754", "Invion": "429113", "Iotronic": "298134", "iPlayer": "417009", "Iris": "231599", "IRON5": "1080890", "Jok Electro": "219128", "Kaon": "298441", "Kathrein": "92994", "Kft": "315643", "Kooltek": "439550", "Kyostar": "219092", "Leader": "219129", "Lemon": "97042", "Lenson": "219071", "Lenuss": "573689", "Leyco": "145133", "Life View": "109108", "Live": "222476", "Lorenzen": "93347", "Lumax": "521161", "MAG": "93411", "Manata": "219067", "Maximum": "302941", "Mecatronica": "441583", "Media Price": "435336", "Mediasat": "439249", "Mediasystem": "600423", "Megasat": "458490", "Meliconi": "226939", "Memorysat": "219091", "Memup": "258417", "Meosat": "595517", "Micro": "97159", "MICRO ELECTRON": "729502", "Mirasat": "418016", "Moussier": "219058", "MTCC": "451970", "Multimo": "219068", "MVision": "420155", "Mysat": "116403", "Necvox": "279307", "Nedis": "259425", "NELI": "710776", "Neotion": "314369", "Neovia": "287220", "Neta": "288520", "Netgear": "220183", "Netgem": "291081", "Neuhaus": "93813", "New Line": "93821", "New Sat": "419514", "Nextwave": "97232", "Ninetech": "315089", "Noda": "339970", "Nokia": "93856", "Notonlytv": "547428", "Npg Tech": "307491", "Omenex": "103724", "Ondial": "276661", "One For All": "93953", "Optex": "218131", "Opticum": "422929", "OPTIMUSS": "1085970", "Orton": "546718", "Pace": "94047", "Patriot": "396322", "Phonotrend": "219085", "Pixx": "290006", "Pkd": "236715", "Pmb": "97370", "Protek": "97410", "Pyxis": "301843", "Qmedia": "427617", "QVIART": "1046374", "Radix": "94393", "Rainbow": "97432", "Reycom": "416749", "Rollmaster": "219574", "SAB": "434856", "Sat Man": "219056", "SATIX": "677756", "Seeltech": "314989", "Selfsat": "446755", "Septimo": "260673", "Servimat": "366144", "Set one": "509552", "Shoi": "504272", "Skyplus": "289945", "Skyworth": "325131", "Slingmedia": "427745", "Smart Line": "139562", "SOGNO": "854765", "Starcom": "95067", "Starland": "234236", "Storm": "95118", "SVS": "235082", "Systec": "262528", "Tahnon": "339082", "TCL": "290364", "TDT BOSTON": "693703", "Technomate": "311151", "Technosonic": "224749", "TechnoTrend": "266002", "Tecsat": "527877", "Tekcomm": "226787", "Teleciel": "219062", "Teleco": "116410", "Telenet": "237262", "Telesystem": "116414", "Televes": "235266", "Telit": "99063", "Telsky": "460232", "Tempo": "95316", "Thomsom": "225989", "Titan": "666593", "Tonna": "219046", "Topachat": "317949", "Topfield": "274462", "Tracer": "95429", "Trekstor": "293728", "Triax": "95455", "Tvnum": "545524", "Tvonics": "431595", "TV-Star": "97861", "Twinner": "219070", "Univers": "391254", "Univision": "298297", "VALUELINE": "699433", "Vantage": "218153", "Vaova": "428537", "Videoweb": "599866", "VIEW 21": "739828", "Visionic": "263163", "Visiosat": "219048", "Volcasat": "490378", "Vu+": "572155", "We Digital": "448485", "Winstec": "291126", "Wisi": "95835", "Wiwa": "329474", "Wizz": "459247", "WWIO": "1122123", "X Trend": "441655", "X-Com": "273709", "XEOFIX": "669814", "XTREND": "727242", "ZAAP": "1164886", "Zehnder": "95911", "Zircon": "138935", "1ATTACK": "671544", "2XL": "521286", "3D SOUND LABS": "1182646", "3M": "90430", "4u": "315992", "A4 Tech": "90440", "Abyss": "139404", "Acme": "217063", "Acomax": "294147", "ACOUSTICSHEEP": "1072331", "Actto": "396706", "ADL": "139407", "ADN": "139408", "Advance": "235475", "AEDLE": "1025264", "AERIAL7": "570678", "AFTERSHOKZ": "748888", "Agef": "90507", "Aiaiai": "472917", "Aircoustic": "614295", "AirDrives": "499711", "Akashi": "315529", "AKG": "90540", "Alecto": "221172", "Alesis": "285875", "Allen & Heath": "479146", "ALPHA AUDIO": "1066359", "Alpine": "90607", "Altai": "96075", "Aluratek": "564826", "Amarina": "272489", "American Audio": "217958", "AMPLICOMMS": "738051", "ANCUS": "1047026", "Ansonic": "138913", "Antec": "90648", "Approx": "293554", "Aquapac": "103778", "Arctic Cooling": "329712", "Arkon": "96108", "Artwizz": "367041", "AS": "90724", "ASTELL & KERN": "851138", "Atari": "90758", "Atomic": "90773", "Atomic Floyd": "546790", "ATTITUDE ONE": "855923", "AUDEZE": "667317", "Audio Chi": "549672", "Audio Phony": "267671", "AUDIOFLY": "755627", "Audioquest": "96147", "Audio-Technica": "235521", "Awei": "397035", "B & W": "90837", "B&O PLAY": "1121937", "Bandridge": "96173", "Bazoo": "326795", "BEATS": "521393", "BEATS BY DR.DRE-FAKE": "803312", "Beewi": "512674", "Behringer": "235529", "Belkin": "140259", "Bench": "366100", "beyerdynamic": "90982", "BIOWORLD": "1118056", "BLACK MARKET": "855819", "BLOC&ROC": "1102698", "BLUE": "1191144", "Blue": "96221", "Blue Micro": "573804", "Bone": "454215", "Bookeen": "490652", "BOOMPHONES": "693799", "Boss": "91081", "BRAINWAVZ": "676492", "Breo Sport": "501305", "BRITISH AUDIO": "1166032", "Brookstone": "575002", "BROWNIZ": "676338", "BST": "116279", "BUDDYPHONES": "1255391", "BYZ": "736946", "CAMPFIRE AUDIO": "1143413", "Campus": "139421", "Canyon": "282163", "CARDAS": "875659", "Case Logic": "234494", "Cellular Line": "91285", "Celsus": "452260", "Cepewa": "513163", "CHICA VAMPIRO": "1174330", "Chord & Major": "1126733", "Cirkuit Planet": "476368", "Ckp Live": "601848", "Clarion": "91343", "Clementoni": "227085", "Cliptec": "452163", "CO:CAINE": "700045", "Code": "574998", "Codiac": "142569", "Colors": "327689", "Coloud": "544787", "Connect": "271693", "Connectland": "328247", "Cool Device": "447970", "Coolbox": "527274", "CordCruncher": "850587", "Cortex": "508717", "Cowon": "310831", "Cresyn": "427301", "Cyber": "234075", "CYBERNETIC": "667320", "Cyberwave": "91495", "CYW": "728388", "Dacomex": "272896", "Dalap": "234072", "DC Comics": "601564", "DCI": "568786", "Dea": "91543", "DEA FACTORY": "683503", "Defender": "321792", "degrees": "1088134", "Delta": "91573", "Dexim": "505488", "DGM": "366577", "DIESEL MONSTER": "770808", "Digifi": "568740", "Digital electronique": "327677", "Digitus": "91619", "DITMO": "682929", "DJ Tech": "445280", "Dolce Vita": "426422", "Dreams": "435795", "Dunu": "451280", "e5": "416206", "Earcandi": "1206706", "EARIN": "1163392", "Earsonics": "514405", "EBTEK": "1107657", "Ecko": "232859", "Ed Hardy": "454118", "EDC": "235728", "Elecom": "306511", "Elro": "91858", "Elveco": "142574", "Elypse": "426437", "Elyxr": "1187716", "Eminent": "236886", "Eneride": "574658", "Enermax": "338684", "ENIGMACOUSTICS": "1256939", "ENZATEC": "593998", "Erard": "235550", "Eskuche": "549955", "ESTRELLA": "1252452", "Etymotic": "339031", "Eurosound": "91976", "ewent": "800534", "EXEZE": "1155217", "Expelec": "233273", "Explay": "329504", "Exspect": "326064", "Extreme": "261511", "FANNY WANG HEADPHONE": "671250", "Fantec": "339531", "Fatman": "433391", "FBI": "733924", "Fender": "416335", "FERRARI LOGIC3": "847284", "FIDUE": "1067408", "Fiio": "458941", "FINAL AUDIO DESIGN": "670411", "Fischer": "92104", "Flair": "92117", "FLAVR": "1192492", "FLIPS AUDIO": "1083782", "Fnac": "103743", "Focal": "96650", "Fostex": "96659", "Fujikon": "234079", "Fujitsu": "92223", "Furutech": "563639", "G&B": "1230375", "G&Bl": "233150", "GADGET SHOP": "685955", "GameOn": "519513", "G-Cube": "452024", "GEEKO": "1140350", "Geemarc": "224274", "Gembird": "314229", "Generic": "290258", "German Maestro": "516153", "GIFTING": "1197835", "Gigabyte": "96709", "GIZZYS": "758211", "GKIP": "697737", "Glam Rox": "459759", "gogear": "1142293", "Golden Tech": "233272", "Goldring": "220823", "Goodis": "811247", "Gorsun": "453830", "Gourmandise": "588510", "Grado": "115339", "Grape": "486053", "Graphics": "306657", "GREEN E": "1132964", "Groove": "235881", "H2O Audio": "428198", "HALO": "509813", "Hamlet": "225769", "Hapena": "146627", "Harman-Kardon": "92528", "Hartig+Helling": "92535", "Havit": "398675", "Headmusic": "317162", "Headset": "235887", "Hedkandi": "458558", "Helios": "219101", "Hella": "92582", "HESTEC": "1069228", "Hexakit Skin Pack": "524138", "HIFIMAN": "667325", "Hi-Fun": "503465", "HINIC": "756345", "HIP STREET": "698463", "Hobby": "220573", "Hori": "326684", "House of Marley": "1125967", "Hualipu": "505032", "Huawei": "317735", "HUMANTECHNIK": "803799", "IBASSO": "744812", "I-Beat": "398913", "Ibox": "398932", "Icidu": "440726", "Icon": "328758", "Iconnex": "329819", "Ifeelu": "476252", "Ifrogz": "446751", "Igo": "322237", "IHIP": "598631", "I-Mego": "398957", "IMG Stage Line": "449844", "IMPERII": "1175574", "In Phase": "417692", "IN2": "732675", "inCarBite": "873423", "Incipio": "499046", "Innovate": "328762", "Intec": "279663", "In-Tune": "521675", "Irhythms": "428318", "iSkin": "317866", "Isound": "416103", "ISY": "595654", "ITC": "92855", "I-Tec": "228299", "ITek": "274683", "IWORLD": "476831", "J&Y": "415048", "J. E. Schum": "307128", "Jabra": "261248", "Jam": "399064", "Jaybird": "495619", "Jays": "435028", "jazwares": "834149", "Jb System": "231905", "JES Collection": "436498", "Jess": "219224", "JH AUDIO": "693091", "JIAXU": "1094920", "Jivo": "441383", "Jlab": "433859", "JOK": "142644", "Joystyle": "601436", "Joytech": "220166", "Joytronic": "454012", "JUST DANCE": "851309", "Jwin": "260553", "KAM": "220525", "Kanon": "418887", "Karman": "103410", "KEF": "93004", "KENNERTON": "1133143", "KENU": "873921", "KEYOUEST": "1028757", "KEYSIU": "710098", "KIDDESIGNS": "544659", "KIDZ GEAR": "836772", "KIDZSAFE": "1066746", "Kikkerland": "489024", "Kinyo": "220436", "Klipsch": "220529", "KLTRADE": "1074817", "Kng": "422458", "Kool Sound": "427466", "Koopman": "260230", "Koss": "93123", "Kove": "453200", "Kraun": "306944", "KRK": "285961", "Kukuxumusu": "499913", "KURIO": "736240", "LASMEX": "728630", "LAVOLTA": "834850", "Lazerbuilt": "224280", "LDLC": "429186", "LEAPFROG": "917333", "Lenovo": "311165", "Lifetime": "222475", "Lindy": "93305", "Little Marcel": "575001", "Little Star Creations": "547307", "Logicom": "103735", "Loooqs": "1103002", "LOSC": "1230436", "LQP": "850574", "Lygo International": "320591", "Mac Mah": "608206", "Madrics": "329497", "Mad-x": "419893", "Magisound": "234081", "Magnat": "93422", "Major": "93435", "Maloperro": "439199", "Marantz": "93459", "MarBlue": "1070909", "MARSHALL": "804642", "Marvel": "270810", "Master": "103833", "MASTER&DYNAMIC": "1129350", "M-Audio": "317018", "MAXAMPERE": "810506", "Maxxtro": "224415", "Mcad": "265215", "MCL Samar": "323216", "MDC": "93527", "Me To You": "451195", "Media Express": "425320", "MEELECTRONICS": "626168", "MEENEE": "846909", "MERKURY INNOVATIONS": "527351", "MEZE": "791577", "MG Itex": "145033", "Mi": "399939", "Microsoft": "93621", "Microspot": "93623", "MIDBASS": "1021037", "Mielco": "434318", "Ministry of Sound": "272350", "Mitchell & Johnson": "1150700", "Mitone": "270064", "Mitsubishi": "93667", "Mix Style": "452424", "Mlb": "476063", "Mobilecast": "547178", "Mobilegear": "419023", "Modecom": "612856", "MOKI": "805894", "Monacor": "93695", "MONOPRICE": "830060", "Moshi": "449691", "MOTÖRHEAD PHÖNES": "804153", "Mr Men": "435980", "Mr. Handsfree": "287179", "MRSPEAKERS": "1072553", "Mtv": "366790", "MTX Audio": "339839", "Multilaser": "431821", "Musical-Fidelity": "93763", "Musicman": "338418", "Muvit": "548224", "MY DOODLES": "1095556", "My Little Pony": "546613", "My Way": "283388", "MYKRONOZ": "874488", "NAD": "93774", "Natec": "445591", "Nathan Multimedia": "320644", "Ndeo": "329567", "NEKLAN": "711203", "Neonumeric": "306070", "Network": "93809", "Newtech": "278204", "Nextbase": "288466", "Nike": "93837", "Nintendo": "93841", "Nixon": "458730", "No.1": "400250", "Noble": "270283", "NOONTEC": "458166", "Novistar": "612112", "NU FORCE": "521682", "Numark": "218232", "OCULUS": "1109394", "OID Magic": "1183663", "ONANOFF": "736015", "ONE DIRECTION": "805039", "ONE SOUND": "745210", "OnePlus": "1203242", "Onkyo": "93954", "Onyx": "149365", "Oppo": "400320", "Opus": "113090", "ORA": "103717", "Osaki": "329323", "OTL": "625311", "Out of the blue": "339807", "OUTDOOR TECHNOL": "745359", "Over Board": "508392", "Pataco": "273358", "PAW PATROL": "1163887", "Peltor": "457836", "Peppa Pig": "480643", "Phiaton": "500857", "Philips O'Neil": "596614", "Philips Swarovski": "453964", "PHONAK": "514629", "Phonia": "142577", "Phonix": "145037", "Phonocar": "94161", "PHONON": "667328", "Piranha": "94184", "Pirelli": "94185", "Playfect": "544926", "Pleomax": "329249", "Pole Star": "103757", "Polk Audio": "97373", "Porsche Design": "94243", "Port": "282319", "Power Star": "605876", "Powerdynamic": "223217", "Premium": "218239", "PreSonus": "599084", "Printlight": "142567", "Pro.2": "94310", "Prodipe": "415869", "Pro-Ject": "116307", "Proporta": "316562", "Prostima": "403921", "PSB": "224054", "Puma": "94355", "Puro": "400592", "Qonix": "274382", "QTX": "225982", "QUARKIE": "745361", "Qube": "460200", "QUDO": "1157404", "Quicksilver": "451007", "QUIETON": "1234998", "Rabbit": "113647", "Radiopaq": "509197", "Raidsonic": "314779", "Rapoo": "452415", "Raptor Gaming": "321858", "Raxconn": "507098", "Razer": "316874", "READY2MUSIC": "1122169", "REC8": "835011", "RECCO": "596102", "RED4POWER": "674964", "Reekin": "455696", "Reloop": "270067", "RETRAK": "676423", "RHA": "673475", "Ritmix": "429541", "R-MUSIC": "1176190", "ROCK JAW": "1024621", "Rocking Residence": "611185", "Roland": "220193", "Rony": "103772", "Ross": "94583", "RUGBY DIVISION": "1075512", "RUNPHONES": "1117243", "RUNTASTIC": "770554", "RYGHT": "671370", "Sadim": "142570", "Saitek": "94666", "Saiyo": "452626", "Samson": "232885", "Sandberg": "426452", "Scholastic": "502315", "Scosche": "325275", "SECTION8": "670281", "Sennheiser": "94824", "SENNHEISER-FAKE": "1127237", "Setty": "1158880", "SEVA IMPORT": "1121291", "SHARK BISCUIT": "625954", "Shike": "329753", "Shure": "220957", "SKINNYSOUND": "697486", "Skpad": "457272", "Skullcandy": "325298", "SLEEK AUDIO": "545412", "SLEEPPHONES": "1119517", "SMART SYSTEM": "1107842", "SMS": "227234", "SMS AUDIO": "737890", "Snakebyte": "327857", "SOGT": "1155655", "SOL REPUBLIC": "712532", "Sonic": "113140", "Sonorous": "440126", "Sonus Faber": "116311", "Soul": "270070", "Soundlab": "97673", "SoundMagic": "544936", "Soyntec": "297844", "Speed Link": "283163", "Spyker": "314672", "Stagg": "430511", "Stanton": "149920", "Stax": "95082", "Steel Series": "437068", "Studioline": "95133", "SUOJUN": "1108655", "SUPER BASS": "753374", "Super star": "97743", "Superlux": "149259", "Sven": "314794", "Swarovski": "95184", "Sweet Years": "451084", "Sylbert": "142562", "TabZoo": "1037713", "TAIDEN": "1145677", "takeMS": "302154", "Takstar": "316423", "Targus": "140806", "Tascam": "115995", "TEC PLUS": "1133574", "Teccus": "416503", "Technics": "95256", "Temium": "427966", "Templar": "218253", "The T.Bone": "544939", "Thesys": "416378", "THINKSOUND": "667330", "Thrustmaster": "95371", "Time4Tech": "1200705", "TINTEO": "808233", "Titanum": "329805", "TNB": "1109172", "TONINO": "499226", "TOYS R US": "745207", "Transcend": "288846", "Transmedia": "416870", "Travel Blue": "396324", "Trendz": "456897", "Tribe": "420170", "TRINITY": "1196371", "TT ESPORT": "599186", "Tubesurround": "422926", "Tunewear": "416965", "Turbo X": "295934", "Turbosound": "302746", "TV Ears": "523823", "Twitfish": "1037250", "TX Think Xtra": "291536", "Ubisoft": "95508", "Ultimate Ears": "417696", "Ultrasone": "97872", "UNEED": "1128159", "Uniformatic": "231298", "Uniross": "103720", "Unitone": "97892", "Universal Music": "450519", "URBAN REVOLT": "1040041", "Urban Tech": "505022", "Urbanears": "559015", "Urbanz": "516206", "Uunique": "609372", "V7 Videoseven": "225795", "Variance": "234076", "VEEBEES": "671188", "Veho": "430530", "Velleman": "295853", "Velodyne": "227367", "Venom": "223167", "Vestax": "233767", "Vic Firth": "480283", "Vivanco": "95670", "V-Moda": "438967", "Vox": "139927", "VST": "287132", "WAATECK": "1105464", "WATS": "725061", "Wavemaster": "287697", "WESC": "455158", "Westone": "453865", "Wintech": "338484", "Wize & Ope": "600905", "Wraps": "1162825", "X-1": "855935", "Xqisit": "479965", "XSORIES": "723556", "Xtreamer": "561080", "XX.Y": "848727", "Yougs": "500466", "Yours": "418561", "YURBUDS": "665237", "YZSY": "1236267", "Zagg": "476997", "Zalman": "327289", "Zenec": "308887", "ZEST": "493774", "ZIPBUDS": "671371", "ZIPERD": "869203", "Zip-Linq": "305503", "Zumreed": "455671", "360FLY": "1158275", "Abus": "231117", "ACME Made": "495484", "Actioncam": "545262", "ACTIONPRO": "730833", "ACTIVEON": "1139700", "AEE": "218492", "airwheel": "1140563", "Amyola": "523923", "ANDOER": "1120831", "APOTOP": "736121", "Beaulieu": "224704", "BILLOW": "671201", "Blackmagic Design": "565335", "Bosch-Bauer": "91078", "Braun Phototechnik": "433608", "Braun-Nuernberg": "91098", "Bullet": "225757", "Camlink": "222724", "CAMONE": "1072387", "CHILLI TECHNOLOGY": "749310", "Clickles": "544646", "Contour": "220276", "C-Tech": "221170", "Delium": "440048", "Delkin Devices": "397760", "Disgo": "302900", "DJI": "1068465", "Drift Innovation": "599250", "ELE": "1059512", "E-TIGER": "726412", "EXCELVAN": "1082071", "Eyenimal": "1179555", "EZVIZ": "1161649", "Feiyu": "398218", "Fisher": "92107", "Flip Video": "480428", "FREE RIDE": "727283", "FREERIDERS": "1270096", "Garmin": "260630", "Geco": "503179", "Geonaute": "317779", "Giroptic": "1205979", "GOBANDIT": "699938", "GOXTREME": "1156035", "Guncam": "598642", "Haldex": "398594", "Halterrego": "601425", "Hanseatic": "92518", "HD": "452662", "HIREC": "1181665", "HOMIDO": "1102769", "HTC": "96839", "Hy Technology": "398902", "Insta360": "1193537", "Isaw": "810448", "JJA": "514668", "Jobo": "259316", "Kaiser Baas": "611217", "KEQU": "1269889", "Kitvision": "588226", "Kmax": "415437", "Konix": "226097", "Lava": "271714", "Liquid image": "488786", "Little Acorn": "230118", "L-LINK": "802628", "Loewe": "93334", "MCA TECHNOLOGY": "669248", "Mediacom": "259813", "Metz": "93600", "Mevo": "1211630", "MIO": "325120", "Mobius": "283776", "MOFILY": "1182634", "MONSTER DIGITAL": "1124961", "MYWI": "1157173", "National Geographic Deutschland": "304553", "NAVICOM": "669838", "Nexxt Idea": "450016", "Numaxes": "459421", "OEM": "227637", "OMEGA": "1055223", "opticam": "527943", "Ordro": "458707", "PANONO": "1164786", "PANOX": "1234472", "PQI": "229521", "Protax": "219543", "Qantik": "1210560", "QimmiQ": "1209608", "QUMOX": "1093868", "R'BIRD": "1235217", "REDKEYS": "1280408", "REMOVU": "1140413", "rePLAY XD": "750972", "RIDEVIZION": "1170571", "ROADHAWK": "869183", "RunCam": "1183057", "Ryval": "445392", "SJCAM": "1087201", "Somikon": "427688", "Spypen": "267291", "SUNNYCAM": "1079717", "Tamron": "95224", "Teamsport": "454975", "TECTECTEC!": "1202556", "TomTom": "268622", "UNIQAM": "1119875", "Universum": "95554", "VOG": "138911", "VUZE": "1224180", "WATER WO": "1183494", "WEMOOVE": "1211271", "Wolder": "417034", "XBASE": "1048466", "Xiaomimi": "472021", "X'TREM": "1269878", "XTREME-CAMERA": "864329", "X-ZERO": "1045466", "YI": "1191054", "YUNEEC": "1108341", "YUTECH": "1077006", "YUWATCH": "1095424", "Zaptub": "611420", "Z-CAM": "1199284", "Zoom": "220266", "4Gamers": "273421", "Adafruit": "1068424", "Adentec": "284747", "ADI": "90488", "Advantech": "501577", "AG Neovo": "225634", "AGM": "96048", "Alapage": "499233", "Albatross": "293089", "Albiral": "265218", "Alienware": "317094", "AMW": "317038", "Amx": "396856", "AOC": "90652", "Aputure": "1025437", "Arduino": "1068433", "ARTHUR HOLM": "833448", "AST": "90746", "Atec": "96132", "ATOMOS": "1073631", "AURES": "608750", "AVidAV": "328025", "Avidsen": "263134", "Avocent": "283688", "Avtek": "1051292", "AXIOMTEK": "1046260", "Barco": "225959", "Bdmc": "431239", "BEETRONICS": "804140", "Belinea": "90939", "Blueh": "442077", "Bluem": "236231", "Bowers": "227813", "Brimax": "229240", "Bull": "103381", "Byron": "264919", "C.Edison": "236223", "Captiva": "308737", "Cdiscount": "340092", "Chimei": "521679", "Chinavasion": "743562", "Cibox": "132037", "Cisco": "265533", "Claxan": "220128", "Cmv": "307467", "Colortac": "325743", "Comelit": "220416", "Commodore": "91382", "Compaq": "91389", "Cornea": "272889", "Cornerstone": "91444", "Crestron": "309523", "CTOUCH": "852767", "CTX": "91483", "Cx": "397644", "Dabsvalue": "297936", "DEC": "91549", "Deltaco": "297664", "Di-Fusion": "316900", "Digital": "266014", "Direction": "318982", "Dynascan": "443633", "Edge10": "1058840", "Eizo": "91810", "Elettrodata": "287901", "Elo Touchsystems": "260170", "Elonex": "225317", "Elyxio": "293346", "Emachines": "273181", "Eneo": "325263", "Envision": "315513", "Escom": "91926", "Esys": "398121", "ETC": "139905", "EURO CLS": "854703", "Eurocase": "449971", "Extron": "398158", "E-Yama": "308892", "Eyestoeyes": "573662", "Faytech": "512658", "FEC": "1067080", "Flytech": "429675", "Formac": "92164", "Fujicom": "366628", "Futura": "226930", "GAEMS": "694939", "Gateway": "113775", "GECHIC": "677347", "Genee World": "1051207", "General Touch": "398414", "Generico": "394138", "Generique": "455373", "GEO": "92311", "Gericom": "96704", "Glancetron": "599602", "GNR": "292590", "GNX": "277567", "GVision": "287982", "Hanns.G": "398621", "Hannstar": "398623", "Hansol": "92521", "Hantarex": "225970", "Hanton": "326884", "Hanwha Japan": "420195", "Harimax": "288473", "Highscreen": "92632", "HIKVISION": "671724", "Hitech": "96808", "Hivision": "260802", "HKC": "320922", "Hpc": "301164", "HUION": "1140409", "Hymer": "92725", "Hyundai It": "435917", "iBoardTouch": "1048105", "IEI": "513118", "IF": "236238", "I-Inc": "366683", "Iiyama": "92754", "IKAN": "1170447", "Imax": "116483", "Infocus": "601846", "Innes": "1057207", "Innopaq": "422147", "Innovative": "275833", "Iolair": "455293", "IPO TECHNOLOGIE": "710375", "Ipure": "314685", "Iqon": "309233", "Irts Display": "316478", "Jdr Computer Products": "305607", "Jean": "116649", "Joy-It": "426605", "KDS": "93002", "Lacie": "115889", "Lancom": "286944", "Legamaster": "94192", "Likom": "93301", "Lilliput": "450799", "Liteon": "93320", "Liteview": "430207", "LUMON": "806723", "Macom": "93400", "Maguay": "443567", "Marshall": "93482", "Maxdata": "220278", "Mermaid": "247951", "Microtouch": "225319", "Mimo": "546625", "MIP": "139518", "Mirai": "283020", "Miro": "93657", "Misco": "93658", "Mitac": "93662", "Modulux": "236281", "Monxx": "200134", "Monyka": "237401", "Msi": "217719", "Multi Q": "140761", "Nagasaki": "512255", "Nano": "400153", "NCR": "113636", "Nech": "139528", "NEWLINE": "813262", "Nfren": "287373", "Nits": "298360", "Novita": "93889", "Nvision": "434895", "NVOX": "626814", "Ocegraphics": "225976", "Octigen": "416325", "Olevia": "422507", "Olidata": "113639", "Origen": "509196", "ORION TECHNOLOGY": "1072740", "Otek": "326251", "Panoview": "326018", "Partenio": "236254", "Partner Tech": "293541", "Pc Note": "314207", "Peacock": "94104", "PEERLESS": "1064441", "Pixmania": "314644", "Planar": "314656", "Polycom": "290344", "Polyview": "311072", "Posiflex": "454038", "POSLAB": "854738", "Princeton": "140762", "Process Tech": "236330", "PRO-FACE": "490302", "Promethean": "599289", "Proview": "116644", "Quato": "94376", "Racer": "235308", "Radius": "97429", "Rapcom": "565662", "RASPBERRY": "1153811", "Rivertech": "402526", "Ryoku": "429374", "Sahara": "297611", "Samko": "325695", "Samtron": "94680", "Sdc": "230429", "Seezen": "454258", "Sensy": "450473", "SEYPOS": "1023528", "Shuttle": "94849", "Sinocan": "854886", "Sliding": "305707", "Smart Media": "559156", "SMARTWARES": "1085332", "Smile": "94928", "SolTec": "806891", "SPECKTRON": "1271409", "Starplus": "236225", "SUN": "95145", "Sunbook": "236222", "Suyama": "418145", "Swedx": "308720", "Switel": "268203", "Synco": "140766", "Syscom": "306909", "Tactyl Services": "509174", "Tandberg": "95226", "Tatung": "95241", "Taxan": "95244", "Tecna": "227461", "Tekneo": "236260", "Terra": "95323", "Textorm": "292822", "Time": "145048", "TOGUARD": "1216514", "Top Elite": "422178", "Top Vision": "113542", "Topcon": "218148", "Topview": "422093", "Totoku": "490208", "TPV": "455268", "Transtec": "97834", "Twinhead": "95500", "Unika": "139573", "Value": "301904", "Vibrant": "218031", "Victor": "95629", "View&Sonic": "523428", "Viewell": "418802", "Viewsonic": "95640", "VITY": "855027", "Wacom": "140253", "Walimex": "440800", "Wewa": "311092", "Wincor Nixdorf": "433078", "Winmate": "232336", "Winsonic": "309416", "Wisetech": "306504", "Wyse": "95868", "X2gen": "311093", "Xiod": "295933", "Xpola": "435308", "Yashi": "220719", "Yuraku": "434476", "Yusmart": "325776", "Zenith": "95918", "3-D-Labs": "220143", "A Video": "439985", "Acoustic Solutions": "285131", "Admea": "316797", "Advance Acoustic": "307317", "Aitro": "418833", "Alco": "297826", "Alize": "308708", "Altrasonic": "367106", "Amuser": "421828", "Apex": "268550", "Arcam": "90674", "Artman": "338587", "ASTD": "527220", "Astron": "103755", "Astry": "307566", "Atacom": "310841", "Atoll Electronique": "149358", "A-Trend": "96021", "Audiobahn": "234288", "Bazzix": "510251", "BBK": "287984", "Becker": "90916", "Bellagio": "310809", "Bloom": "310774", "Blue:Sens": "366455", "Boghe": "327391", "Bom": "366528", "BRILIANT": "733640", "Brothers": "297712", "Casablanca": "292286", "Cdmc": "314425", "Cello": "308935", "Changjia": "528151", "Cilo": "394537", "Cinetec": "310274", "CJ": "430754", "Classé Audio": "116282", "Contel": "415243", "Curtis": "234029", "Cybercom": "96385", "Daytek": "91533", "Daytron": "218840", "Delphi Grundig": "315920", "Desay": "261748", "Difrnce": "432248", "Digix": "327823", "Digixmedia": "293284", "DK Digital": "91620", "DMC": "268573", "Dmtech": "294115", "Doriland": "428908", "E:Max": "320818", "E-Dem": "315018", "Electrocompaniet": "268553", "ERA": "226011", "EVD": "659440", "Fifty": "482855", "FIT": "476344", "Fredikson": "269533", "Funai": "92232", "Giec": "301563", "Golden Rich": "291949", "Gowell": "340009", "GVG": "326394", "Harmony": "221062", "Haymedia": "327400", "HIGH-TECH PLACE": "1162353", "Hillteck": "273148", "Himage": "271942", "Home Electronic": "274154", "Home Power": "325702", "Homita": "315388", "Inovix": "315971", "Kaford": "544680", "Kazuki": "427380", "Keyplug": "306877", "King Vision": "367109", "Kiss": "226026", "KLH": "220528", "Kxd": "301580", "Laboratory": "218854", "Lexia": "238606", "Lifetec": "93296", "Limit": "308841", "Linn": "93312", "Linuo": "399684", "Liros": "339174", "Loomax": "289963", "Luxman": "93381", "Maitec": "93433", "Mc Intosh": "93523", "Meridian": "140307", "Messo": "317312", "Micromega": "140308", "Minton": "234190", "Mizuda": "307525", "MP ELECTRONICS": "865856", "Myryad": "146611", "N.T.P.": "305130", "Neuston": "291950", "Newtone": "323223", "Ninco": "478414", "NRJ": "430542", "Nu": "400276", "Olitec": "220186", "OLSENMARK": "659672", "Oritron": "232416", "P&J": "339100", "Palladine": "316732", "Panda": "229488", "Phocus": "324214", "Pilot Nic": "314985", "Primare": "219366", "Prinz": "94288", "Pro²": "315013", "Projectiondesign": "297563", "Promaster": "284705", "Proton": "94338", "Quali-TV": "338490", "Quartek": "339173", "REX": "94500", "Rotel": "94588", "Rowsonic": "219579", "SB": "422288", "Scanmagic": "141075", "Seal": "419667", "Seelver": "297904", "Sevic": "301573", "Shanghai": "234829", "Sherwood": "94843", "Shinco": "115075", "Shindo": "294055", "Siemssen": "115510", "Siltex": "288995", "Simbio": "366395", "Sinivision": "273966", "SMC.Stallmann": "94926", "Soniko": "219231", "Speed Sound": "234404", "Starclusters": "310204", "Starlite": "95070", "Stein": "287185", "Strato": "113141", "Sumvision": "316913", "Sunwood": "145136", "Superior": "95166", "SVC": "222485", "Takada": "401404", "Techlux": "419321", "Techma": "432117", "Technika": "274618", "Techtron": "457521", "Tecnimagen": "113540", "Teknika": "367110", "Tendances": "310363", "Texon": "222907", "TG": "318978", "Thule": "95374", "Transconti": "149305", "Trans-Continents": "319193", "Transgear": "327809", "Trinity": "367014", "TSM": "95477", "Tyme": "452449", "Universal Uos": "95552", "Upteck": "317974", "Vatech": "493547", "VEREZANO": "802646", "Viewfun": "420171", "Voxon": "269521", "Voyager": "95695", "Vtrek": "401838", "Wilson": "95810", "Xeos": "291750", "Xonum": "290992", "Yamakawa": "98021", "YARVIK": "659449", "Zanon": "291495", "Zicplay": "301179", "3 Suisses": "142576", "Aigger": "326538", "ART&CUISINE": "699928", "Avdi": "231619", "Azura": "421088", "BOP": "231621", "Botti": "512346", "Carlton": "91237", "Carrera": "91243", "cecotec": "1045045", "Changli": "443741", "Clean Maxx": "365874", "Concept": "288732", "Cora": "222519", "Di Quattro": "233004", "Diana": "91600", "Dicaff": "218082", "Dieselit": "317767", "Duke": "233187", "Ecova": "231638", "Eltronic": "303415", "Esse 85": "222769", "Eternity": "339256", "Euroflex": "290343", "Ferrari": "92073", "First": "539376", "Fiseldem": "222770", "Fogacci": "92153", "Fortex": "398278", "Go Travel": "398460", "Goodway": "218508", "Hailo": "92488", "Hinari": "92638", "Hoffmanns": "1072703", "Hugin": "139898", "Hydro": "486265", "Imetec": "92765", "INTERIOR": "1073215", "Jagua": "512676", "JRD": "1232716", "Jrr Electronique": "314840", "Kaercher": "92955", "KEIM HOUSE": "1211258", "Kiti Pro": "500953", "Kiwi": "232568", "KLINDO": "1214332", "KOENIC": "595652", "Laurastar": "93231", "Leifheit": "93256", "L'El-It": "222773", "Libellule": "263645", "Maitop": "1211315", "Metalnova": "222772", "Micromark": "221055", "MONEUAL": "562520", "Nordland": "268435", "Pfaff": "599573", "Practica": "305837", "Prodis": "139952", "Prym": "450416", "Remington": "94482", "RGK": "231846", "Rhonalvap": "285047", "Robby": "231620", "SANEO": "1028072", "Saturn": "97544", "Saxel": "222777", "SHG": "94844", "Shinelco": "217068", "Silva": "274357", "Silverstone": "1167300", "SMART STEAM": "1202329", "Speedline": "310848", "STEAMONE": "626703", "Sunbeam": "95147", "TECHNO": "95259", "TEKNOSTEAM": "1265467", "Travel Smart": "283253", "Trikado": "298119", "Vapex": "231625", "Vapoline": "488959", "Vaporella": "231622", "Vapornet": "594100", "Vitek": "290366", "Xelance": "314728", "XSQUO": "1142697", "Zephyr": "570499", "5FIVE": "1252653", "A.Marque": "224219", "Ankarsrum": "513159", "Aura": "96152", "Bamix": "259427", "Beaba": "287888", "Bellini": "309419", "BEST OF TV": "687541", "bianco di puro": "1174287", "Bimar": "146975", "Blendicook": "1207924", "Blendtec": "418842", "Brabantia": "91089", "Brano": "416179", "Buffalo": "1105356", "CEEA ROBOT MAXI CHEF": "692500", "Chef": "329584", "Climaselect": "513457", "Comelec": "270792", "Conti": "273791", "Cooks Professional": "1255869", "CUCCINA": "689433", "Cucina": "454430", "Cuisichef": "491680", "Cyril Lignac": "1154279", "Dalkyo": "139932", "Detoximix": "1217120", "DOMOTECH": "1028175", "Ds": "272255", "DURAND DUPONT": "1143965", "Dynamic": "368254", "E.ZICHEF": "1184964", "ECO-DE": "804243", "ELEKTRA LINE": "1166826", "Esge": "91928", "Essentials": "282801", "ETA": "223558", "Euro Wave": "315807", "Eurowave": "511796", "Feller": "426742", "Figuine": "366095", "Flama": "218052", "FLAVORFULL": "1139250", "Foodmatic": "1226847", "Franklin": "92184", "Fritel": "91353", "G21": "1045108", "Gio'Style": "240811", "GOURMET GADGETRY": "1101634", "GOURMET TOOLS": "1214914", "GSC": "1024095", "Guangdong": "619155", "Hagen": "660633", "Happy Cook": "398657", "Hawkins": "229298", "HELD": "1102038", "Hendi": "270060", "HERENTHAL": "1264361", "Herzberg": "1208236", "Homekraft": "1204898", "Homemaker": "229308", "Ideas": "293704", "Jata electro": "1103022", "Jtc": "263150", "Jupiter": "92932", "Kai": "482832", "Kisag": "489936", "Kitchen Cook": "491594", "KITCHEN FRIDAY": "1158609", "KITCHEN MANAGER": "694892", "KITCHEN-GRAND-C": "802572", "KUVINGS": "687605", "Laica": "227012", "Lenoir": "113512", "Lifestyle": "284743", "LITTLE BALANCE": "1074037", "Look For": "272328", "LOUIS TELLIER": "1105461", "Luxe": "234739", "Magic Bullet": "427621", "Magic Maxx": "339179", "MAN": "220735", "MARC VEYRAT": "672548", "Martin Berasategui": "1217260", "MAYBAUM": "453404", "Melissa": "113288", "Mini Chef": "340044", "Miogo": "1203241", "Mix-N-Mix": "523387", "Montiss": "317644", "Mr.Magic": "403133", "Mywave": "546614", "NEWCHEF": "1144497", "Nikai": "323786", "Ninja": "598219", "Noon": "457940", "NUTRIBULLET": "815166", "Ohmex": "488784", "OmniBlend": "1064546", "ONE TOUCH BULLE": "1119113", "Optima": "93981", "Orava": "273509", "Oxo": "226772", "PANGEA": "755897", "Passat": "338742", "Philips AVENT": "262788", "PRADEL PREMIUM": "1023812", "Prolectrix": "416862", "Red Line": "231292", "Redmond": "94444", "Relaxdays": "546018", "Robot Coupe": "366099", "Ronic": "219584", "ROSLE": "1153843", "Salter": "227014", "Samix": "508124", "Saphir": "97540", "Scaroni": "115274", "SCHEFFLER": "1217607", "Schenzhen": "314841", "SCHMIT": "1174480", "SECRET DE GOURM": "1028769", "SelectLine": "421801", "SHAKE N' GO": "848388", "Shivn Feng": "401052", "SINOTECH": "864323", "SMOOTHIE XPRESS": "1160398", "Sonashi": "261613", "Superchef": "530414", "Supercook": "232756", "SWEETALICE": "696041", "Tarrington House": "430744", "Team Kalorik": "513008", "Terraillon": "95326", "T-Fal": "440192", "Trebs": "499919", "TRIBEST": "856791", "Turbotronic": "528525", "TV UNSER ORIGIN": "1070787", "Ultramaxx": "1101703", "Venteo": "442611", "VitaMix": "418942", "Vivre Mieux": "1205137", "Vortex": "95693", "Waring": "293836", "YAMMI": "1026427", "YUECHING": "1270311", "ZEN & PUR": "1210095", "Zyliss": "235359", "360 SWEEP": "1144565", "A & C": "306069", "Agait": "570219", "Agama": "610121", "Alfatec": "226786", "Aquavac": "228374", "Arle": "231845", "ASPIROMATIC": "1104652", "ASPIRON": "1038105", "Astel": "307577", "Bavaria": "90904", "BE PRO": "1199194", "Beldray": "232399", "Birum": "231808", "Bissell": "224099", "Bliss": "91029", "Blitz": "247823", "BLUE BELL APRC": "692499", "bObsweep": "1211333", "Bork": "293093", "Bricotech": "310808", "Britania": "323134", "Broszio": "96247", "Build Worker": "446999", "Builder": "263535", "Car +": "589645", "CENOCCO": "1076306", "CEVIK": "693925", "Cevylor": "231832", "Clean Star": "327499", "Clean Up": "485598", "Cleanfix": "283720", "CLEANING": "1039767", "Cleanmate": "415407", "Contact": "103747", "Corner": "437058", "Crazy": "259971", "Cyclonia": "538304", "Davo": "231836", "Daya": "316489", "DEEBOT": "736089", "Defort": "611276", "Delfin": "326032", "Delta Jet": "231842", "Deltaspire": "231826", "Dexter Power": "441008", "Dilem": "218048", "Dimin": "231830", "DIRT BULLET": "442222", "Dirt Devil": "91629", "Dirt Hunter": "231835", "Dolce Casa": "601587", "E.Ziclean": "545364", "Earlex": "224129", "Ecodrop": "594067", "Ecovacs": "446995", "Eder": "231822", "Edison": "269928", "Eio": "296127", "El Fuego": "1084292", "Electro-Line": "234466", "Electromix": "452677", "Elekta": "139936", "Elektro Maschinen": "435757", "Elem/Technik": "510134", "Elin": "99062", "Emer": "226712", "Eufab": "91947", "Eurasia": "450466", "EUROBOTS": "713290", "Eurom": "284726", "EUROMENAGE": "1101677", "Ewbank": "260992", "EWT": "91993", "Excelsa": "471797", "Expressline": "231838", "FAM": "270215", "Far Tools": "237673", "Favel": "324158", "Feider": "421045", "Fein": "92061", "Feroe": "231843", "Fersen": "231815", "Festool": "148972", "Fiac": "459514", "FIELDMANN": "686108", "Finetech": "1191140", "Flex": "92125", "Floor Zoom": "1200747", "Gardena": "92269", "Germatic": "298281", "Ghibli": "271417", "Gisowatt": "222771", "Glen Dimplex": "320143", "Goblin": "222732", "Goodyear": "262739", "Greenworks": "237414", "Guzzanti": "288730", "Haeger": "140851", "HETTY": "1204687", "Hilti": "229303", "Holland": "231849", "Home Angel": "283767", "HOME CLUB": "1048603", "Home Talent": "231844", "Homefriend": "283159", "IDE Line": "92745", "IDEAL HOME": "669226", "Impex": "103777", "Incasa": "266001", "Indomo": "329271", "Intertronic": "92825", "Irobot": "337956", "Ironside": "96903", "Ismet": "92847", "Italvas": "231824", "JE CHERCHE UNE": "1121241", "K&": "739986", "Kawasaki": "92996", "KENNEX/TB": "113509", "KENSTON": "1252481", "Kinzo": "96968", "KOMOBOT": "1160313", "KOTEL": "736299", "Kraft": "320415", "Kress": "93143", "L'Aspirateur": "566046", "Lavor": "93234", "Lavorwash": "97027", "Leman": "282803", "Leroy Merlin": "263160", "Lervia": "301868", "Linea Casa": "471570", "LINEA TIELLE": "1260876", "Liv": "271359", "Mac Allister": "278684", "MAGIC UV": "1114342", "MAMIROBOT": "736422", "Mannesmann": "93452", "Mastrad": "294114", "Matrix": "315386", "Mauk": "854958", "MAX": "93505", "Maxipower": "522914", "Mazda": "93514", "Mc Kenzie": "238579", "MD": "1210088", "Mda": "317979", "Meister": "93559", "Mejix": "93564", "Melchioni": "339423", "Michelin": "262344", "Mr Buddy": "608782", "Muter": "231848", "Neato Robotics": "613017", "Necchi": "459694", "NEWTECK": "1097489", "Nilfid": "231850", "Nilfisk": "115088", "Nilfisk-Alto": "415101", "NODIS": "668683", "NOVELLY": "1066062", "Novipro": "393806", "Numatic": "223581", "Numero 1": "313993", "Oase": "93906", "ok.": "595655", "OTOKIT": "851546", "PARIS RHONE": "1102234", "Parkside": "419391", "Perel": "237677", "Performair": "450372", "Performance Power": "227575", "Petit": "231847", "Peugeot": "94143", "Plihal": "231818", "Polaris": "94221", "Power Plus": "94254", "Powervac": "231816", "Practyl": "237878", "Prixton": "429148", "Profi": "94318", "Prologic": "231833", "Promac": "429048", "PROVAC": "730931", "RAVLINE": "842077", "Raycop": "500782", "Redstone": "489890", "Rhino": "97471", "Ribimex": "278817", "Ribitech": "428181", "Ring": "224166", "Robomop": "440839", "Rohs": "599071", "Rondy": "237281", "Rotary": "227479", "RUMBOT": "1159587", "SAUGKRAFT": "1099494", "Sebo": "94797", "Shivaki": "271363", "Shopvac": "231635", "Sidamo": "231821", "Simec": "231624", "Simmons": "225282", "Simpa": "94891", "Simpex": "323978", "Sisal": "231637", "Skil": "94912", "Solfacil": "231831", "Sona": "222758", "Sonnenkönig": "421571", "Sopadis": "286874", "SP`D Clean": "323620", "Sparco": "270068", "Speedclean": "313931", "Spit": "237877", "Stayer": "95083", "Steamatic": "231825", "Stihl": "95104", "Sumex": "510219", "Sunny": "95153", "Super Clean": "329024", "SUPERTEK": "689925", "Swivel": "403214", "Syclone": "548551", "Tango": "305691", "Technic": "231823", "Tekvis": "268265", "Teleshop": "292792", "Terraclean": "222779", "The Boss": "302165", "Thoshiro": "846911", "TLJ": "750889", "Tokina": "95398", "TORNADO": "1037035", "Trendy Color": "272721", "TSB": "231840", "Tudor": "1186405", "Twister": "279604", "Ubbink": "95507", "ULYSSE": "671067", "Vacmaster": "572243", "Varo": "314701", "VAX": "142039", "Vetrella": "222781", "Vigor": "271721", "Vileda": "231346", "Viper": "223169", "Volta": "95687", "Vorwerk": "226721", "Windmere": "95813", "WOLPERTECH": "1199205", "X5 VAC": "1119743", "X6": "811298", "Zinatic": "231809", "ZYGOSHOP": "1064195", "Ambassade": "115020", "Arrow": "90710", "CITIZENS": "744017", "Corbero": "115031", "Domest": "269971", "Fde France": "224133", "Fensa": "319057", "Gebhardt": "265388", "Glem-Gas": "475957", "Husqvarna": "92715", "Jollynox": "225107", "Kehl": "218516", "LA Cornue": "596360", "Laclanche": "265405", "Lofra": "224160", "Luxell": "305847", "Mora": "97197", "M-Systems": "309237", "Mumsig": "433849", "NED": "227487", "New World": "229623", "Oven Plus": "265383", "PER": "265381", "Privileg": "575954", "Restpoint": "511528", "Savoir": "400897", "Segad": "115064", "Setra": "115378", "Siul": "231948", "Sogedis": "265385", "Sonai": "329000", "Technogas": "489294", "Triumph": "143158", "Universal": "340245", "Waltahm": "339314", "Westahl": "549559", "Zanussi-Electrolux": "321644", "3GREEN TECHNOLO": "1161590", "Aaeon Technology": "573691", "AAT": "221014", "Absolut": "227059", "Actina": "295899", "ACTION": "850579", "ADJ": "437419", "Adonia": "1166282", "ADS-Tec": "596172", "Aerocool": "329810", "Akasa": "338481", "A-Link": "338491", "ALIX": "1077558", "Alphacom": "90602", "Alphamedia": "236221", "Alternate": "417836", "ALZA": "732601", "Amazon": "323139", "Amerry": "770222", "ANKERMANN COMPUTER": "713847", "Aopen": "220262", "APC": "224924", "API Computer": "265547", "Aquarius": "223957", "ARI": "1081693", "ASRock": "429402", "Athena": "113685", "Autocont": "295951", "Avaya": "267616", "Avi Micro": "236218", "AVNET": "1064373", "AWOX": "851285", "Axel": "596664", "Axis": "96161", "AZIROX": "1201525", "AZULLE": "1181920", "BACATA": "812508", "Banana": "224567", "Beagleboard": "1051188", "BEELINK": "1165179", "Biostar": "149523", "Birch": "612868", "BLACKLINE": "676301", "BlackStorm": "455636", "Bluechip": "396126", "Bogo": "547455", "Camtrace": "1051260", "CAPTURE": "1225190", "Cheap": "236276", "Chiligreen": "305779", "Chip PC": "418003", "Cirque": "91334", "CITTADINO": "769983", "clientron": "1077591", "Colormetrics": "1075170", "Comfor": "294397", "COMPUDEALS": "805327", "Compunet": "236176", "Compupro": "305361", "Cooler Master": "317891", "Corsair": "327453", "CORUS": "744826", "Crane": "230031", "Cybershop": "236242", "Cybertek": "422654", "Cyrus": "116286", "CZC": "1070013", "Danew": "430205", "Data Graphic": "294408", "Datapath": "220138", "Decimal": "236180", "Depo": "307208", "DG-Micro": "236182", "Di": "1074247", "Differo": "340455", "Digicom": "222810", "Digipos": "1097115", "Digipro": "396327", "D-Link": "220134", "DROIDPLAYER": "1097106", "DTK": "113702", "DUNE HD": "865098", "Dustin": "455880", "Dynamode": "316236", "EALTEC": "1230328", "ECRIN": "1080390", "ECS": "91779", "Egreat": "481120", "EID": "293706", "Ei-System": "139438", "Elitegroup": "441356", "Epa": "315518", "Epatec": "545122", "Erel": "236255", "Ernitec": "840648", "Event": "227123", "Evga": "426447", "Exone": "96595", "Factory": "290566", "Flextron": "598996", "Forcast": "274038", "Foxconn": "338483", "FT": "236261", "Game Lander": "455066", "gecCOM": "833452", "Giada": "548007", "Gigabox": "236226", "Gigasys": "218493", "GOALLTV": "1115043", "Google": "487916", "H96": "1227588", "Hal3000": "598899", "HardKernel": "1086626", "Hardware Outlet": "513452", "HIMEDIA": "1034503", "HIPER": "884702", "Home": "218070", "Honeywell": "92678", "HUMELAB": "1108090", "Husk Tech": "480646", "Hyrican": "113066", "ICARICIO": "728716", "Igel": "92752", "IGGUAL": "803373", "Ikom": "236184", "Impression": "393818", "Infinity": "92786", "Inforsud": "236246", "Inmac": "92794", "Inno3d": "368018", "Integris": "460536", "Intelbras": "327482", "Intermec": "217705", "Intertech": "96899", "Inves": "103400", "IPC2U": "572151", "Itium": "273111", "Jetway": "287384", "Juniper Networks": "403223", "Kaiwin": "217728", "Kapcom": "284692", "Kelyx": "328783", "Kerti": "236259", "KIANO": "675284", "Komputronik": "459461", "KUBB": "1060857", "L.G.L. Dev": "236263", "LANNER": "812701", "LC Power": "315601", "Leadtek": "97034", "Legend": "93247", "Lineane": "236279", "Longshine": "97068", "Lynx": "115049", "Majesty": "231262", "Mansoft": "93455", "Marcopoly": "315398", "MEASY": "1020769", "Mede8er": "543959", "Mesh": "225344", "MGD": "432537", "MIB": "236177", "Micdis": "217733", "Micro Tech": "97161", "Microllenium": "292241", "Micromaxx": "225353", "Microstar": "265048", "Minix": "399992", "Morex": "235639", "MR. MICRO": "1084642", "MSG": "567099", "Ms-Net": "132038", "Multimedis": "93752", "MXQ": "1168614", "MYGICA": "670401", "nabi": "805635", "Nantesmicro": "236257", "Nausicaa": "1204226", "NComputing": "506092", "NDIS": "872558", "Nemo": "218083", "NEOUSYS TECHNOL": "1068697", "Neoware": "288762", "Newdata": "318292", "Nexcom": "500628", "Next": "93826", "NEXXT": "1145984", "Nirva": "236237", "Norrod": "393759", "Novotec": "217734", "NOW TV": "1073778", "NURVO": "836803", "Nutanix": "848761", "Nvidia": "301774", "Oceanet": "236278", "Ocem": "236185", "ODX": "236239", "Oldi": "314386", "One": "301789", "OnePc": "1176423", "OpenHour": "1093697", "Optimus": "309127", "Oracle": "217623", "Ordissimo": "431413", "Orgelec": "276186", "PanOcean": "329975", "Paradise": "220190", "Pc 2000": "94097", "PC ENGINES": "722474", "Pc Tek": "307294", "PC Wave": "236258", "Pc.Kube": "301128", "Pci": "301449", "Pegasus": "94111", "Pegatron": "573497", "Penta": "139545", "Perimetre": "236199", "Phoenix": "94158", "Planet Elektronik": "321293", "Platin": "1170637", "POINDUS": "855798", "Point-Of-View": "261552", "Popcorn Hour": "472477", "Powernet": "288494", "PRAIM": "668024", "Premio": "301548", "Primux": "452340", "PRODVX": "1087701", "Pyramid": "97416", "Q Motion": "284723", "QNAP": "448961", "Quanta": "314084", "Quest": "225276", "Rangee": "428687", "RASPBERRY PI": "713224", "Rikomagic": "808157", "Roku": "418031", "Rombus": "272459", "SAGA": "1225227", "Sapphire": "290954", "SEDATECH": "727299", "Sequence": "220551", "Serioux": "452451", "Simplivity": "1096531", "Sitten": "1068537", "Skynet": "505546", "SolidRun": "1079159", "Sonbook": "269482", "Spacebr": "513239", "Speechi": "1182247", "Staris": "236228", "STORITE": "1044833", "Supercomp": "225987", "Supermicro": "290431", "Surcouf": "293561", "Systea": "545123", "Systeam": "599721", "Tandy": "103379", "Tarox": "286941", "TENGO": "851386", "Tesenca": "236234", "THOR": "735893", "Titeck": "285661", "TIZZBIRD": "724322", "TKF": "236224", "Top Station": "236194", "Traxdata": "95444", "Trend": "95445", "Triline": "294396", "TRONSMART": "1063779", "Tsunami": "220562", "Tulip": "95483", "TWC": "236272", "Twintech": "422179", "Tyan": "298266", "Tysso": "401703", "U.P.I": "274065", "Ubiquiti": "513036", "Ultimo": "236196", "ULTRATECH": "736054", "Ultron": "285508", "Underwood": "113626", "Upvel": "625144", "Veci": "236244", "VECTREX": "1159228", "VEKOBS": "727419", "VENZ": "1170439", "Vero": "297697", "VIA": "95625", "Vibox": "855931", "Vision": "95657", "vivapos": "1050248", "Vivitek": "366970", "VXL": "330226", "Western Digital": "302906", "Wetek": "288512", "Wibtek": "838885", "Winblu": "459531", "Winner": "431265", "Workey": "272375", "XLYNE": "737088", "Xtratech": "329108", "Yatoo": "309418", "Zebra": "95909", "ZEETIM": "1278391", "Zidoo": "1174682", "Zoostorm": "436029", "Zotac": "445483", "180S": "559195", "1IDEA": "476826", "1MORE": "1153054", "2Go": "523017", "4-OK": "683253", "4SMARTS": "1132431", "A+": "482681", "Abe": "396690", "AC": "90455", "AC Unicell": "103746", "Accessorize": "499850", "Accuratus": "285104", "Accutone": "90466", "Addict": "545485", "ADIBLA": "1196516", "ADVANCED ACCESSORIES": "1078430", "AFTERGLOW": "803353", "Agatha R. Prada": "437371", "Agfeo": "90510", "Aiino Style": "507340", "AILIHEN": "1265774", "AIR": "139409", "Akito": "217984", "AKYTA": "689081", "Aliph": "481121", "Allgon": "90582", "ALPHA OMEGA PLA": "1176112", "Alpha Secom": "103796", "AMPLIFY": "1083963", "Andrea": "329792", "Andrew": "90638", "ANIMA": "1139904", "Anycom/RFI": "220194", "APACHIE": "1261522", "Apcom": "479904", "Apple-Fake": "478729", "AQUAMIX": "865851", "Arcas": "598034", "Arcotec": "274112", "Ardt": "417828", "Arp Datacon": "220220", "ART": "103727", "AS-MOBILITY": "1096599", "ASTRO GAMING": "756232", "Aswo": "259657", "AUDÉO": "713023", "Audionic": "676311", "Auerswald": "90785", "AUKEY": "1086216", "AULA": "722421", "Auro": "90789", "Av Link": "366502", "AVANCA": "803359", "Avantalk": "499890", "AVANTREE": "695058", "Avizar": "1097605", "Avo": "90826", "AVO+": "1198413", "Avro": "421043", "Axes": "499118", "Axtel": "548358", "Azona": "140250", "BASEUS": "803786", "BASSBUDS": "917754", "BAT MUSIC": "699247", "Battrex": "271924", "Beeper": "495574", "BenQ-Siemens": "417930", "Benross": "225051", "BERSERKER GAMING": "1256114", "Bhs": "283752", "Bitfenix": "594341", "Black Box": "279067", "Black Platinum": "340400", "Blackberry": "287115", "BLACKBERRY-FAKE": "521659", "Blaze": "224489", "BLOODY": "749094", "blu:s": "1084370", "Blue Star": "103421", "Blueant": "416177", "Bluedio": "480725", "Bluenext": "434387", "Bluespoon": "339939", "Bluestar": "612585", "Bluetake": "318120", "Bluetalk": "433928", "Bluetooth": "435214", "Bluetrade": "310850", "Bluetrek": "317615", "Blueway": "339699", "BLUEXTEL": "1047115", "B-Move": "562532", "BOAS": "1055004", "Body Glove": "237173", "Boeder": "91052", "BOOMPODS": "1077029", "BOOSTER": "853460", "Boulanger": "273621", "BOVON": "1277620", "BOWER": "625738", "BRAGI": "1179334", "Brigmton": "138919", "B-Speech": "318192", "Btk": "433937", "Cabstone": "545126", "CAEDEN": "1168336", "CALIBUR11": "682403", "Callate la Boca": "547926", "Callstel": "451341", "Capcom": "142962", "Cardo": "327455", "CASEINK": "1051493", "Casino Famili": "597589", "Cellink": "292489", "Cellman": "259654", "Celly": "267633", "CHICBUDS": "658813", "Clarity": "338377", "Clip&Talk": "1165619", "Cm Storm": "512675", "Coca Cola": "221015", "Coco": "490608", "Cocoon": "91360", "COLORBLOCK": "687056", "Colorfone": "482238", "Competition Pro": "293707", "Computer Gear": "315598", "Connect It": "434428", "Connected Essentials": "613906", "Connect'Line": "103771", "Contour Design": "141062", "Cosonic": "418645", "Cougar": "1107265", "COWIN": "683172", "crazybaby": "1171713", "Cresyn Industrial": "588488", "CROSSCALL": "770075", "Crypto": "306890", "CRYSTAL AUDIO": "730552", "Cta": "397564", "Cubik": "431402", "Cyber Blue": "450203", "Cyber Snipa": "423028", "Cyborg": "442723", "Dacom": "548418", "DAMSON": "833398", "Datel": "272162", "Dectel": "145017", "Definitive": "220509", "Defunc": "1158080", "DEGAUSS LABS": "723741", "deleyCON": "1036905", "Delock": "314770", "Devia": "471811", "Dextra": "224717", "Dicota": "268405", "DIGITAL SILENCE": "671798", "DISNIX": "1215977", "DIVACORE": "744723", "Doro": "91671", "Dotz": "1140557", "DRAGON WAR": "810993", "Draxter": "419315", "Dreamgear": "415083", "Dymond": "317601", "EAMEY": "1121965", "Earebel": "1162235", "Earson": "509667", "EASARS": "750002", "EASYKADO": "1105302", "Easytel": "221006", "Eblue": "397994", "E-BLUE": "1175611", "ECE": "319673", "Echo": "91770", "E-Dimensional": "457017", "EERS": "827378", "ELESOUND": "1083953", "Elipson": "227326", "ELITACCESS": "1267338", "Elle": "91850", "Empire": "91880", "Emporia": "272931", "Encore": "273448", "Enjoy": "91893", "EPICGEAR": "709916", "Erato": "518267", "Ergenic": "259698", "Ericsson": "91912", "ESTUFF": "683472", "Eten": "292775", "ETIGER": "825975", "Everglide": "427827", "EVIL": "1027722", "EVOLVEO": "1060117", "Excel Com": "103716", "Expansys": "298435", "Exponent": "224400", "Facon": "103791", "FANTIME": "1166075", "FASHION TALKY": "755879", "FEINTECH": "1196530", "Fellowes": "224401", "Fff": "493678", "FIERRO": "1254026", "Fiesta": "232723", "FINEBLUE": "1040162", "FITBIT": "737090", "Fittek": "571115", "Flexus": "420911", "FLUOR": "1125813", "Follow Up": "1227213", "FONEMAX": "713354", "Fonex": "221349", "Fontastic": "92156", "Formosa": "260545", "Freaks & Geeks": "1169996", "Free Style": "431995", "FREEGO": "907873", "FREEGUN": "549521", "Freemate": "543965", "FREESOUND": "864464", "Freewave": "226109", "FRENDS": "770818", "Fresh ‘n Rebel": "1034092", "FUN CONNECTION": "1178904", "Func": "565661", "Fundigital": "504174", "G.GEAR": "1081768", "G.Skill": "431176", "GAMDIAS": "1029318", "GAMEKRAFT": "1062042", "Gameware": "393778", "Gamexpert": "319049", "GAVIO": "558347", "GBK": "433869", "Genesis": "96699", "GG Telecom": "393764", "Ggmm": "489225", "Gigaset": "398437", "Gioteck": "450571", "G-LAB": "1091559", "Glofiish": "482192", "G-MOBILITY": "695035", "GN Netcom": "308822", "Golla": "315878", "GONBES": "806872", "Good Access": "437280", "GoSport": "1172519", "GOUDISE": "1082957", "GP": "92390", "Green": "96745", "Gsm": "270638", "GSound": "321772", "GT": "234332", "Guess": "234971", "HAC": "1029324", "Hagenuk": "92483", "HANIZU": "848360", "HAPPY PLUGS": "696361", "Hds": "233792", "HIBLUE": "743547", "HIDITEC": "1039800", "HIMADE": "1184446", "Hi-Teh": "847861", "HMC": "269931", "HMDX Audio": "509511", "HOCO": "674830", "HONOR": "1099812", "HOODIE BUDDIE": "1091625", "HOUDT": "1084527", "HSINI": "1059245", "Hyperx": "1185479", "I.AM+": "1185146", "IBike": "598471", "ICANDY": "478844", "Ice Watch": "515808", "Icemat": "327782", "ICE-PHONE": "1062988", "I-CREATION": "737962", "Idea": "96858", "Ideenwelt": "563864", "Ideus": "447864", "Idream": "322192", "IGGY POP": "1271184", "IMAZE": "869037", "IMOOVE": "711832", "Impact": "116594", "inateck": "1036901", "Indeca": "326079", "ING": "515298", "Inkclub": "323141", "Inline": "265079", "Interphone": "416428", "Iogear": "307719", "i-Paint": "815244", "ipipoo": "1085852", "Ipone": "569723", "Iqua": "419235", "IS": "1146356", "Isotech": "316871", "ISP": "92851", "IT7": "740051", "I-Tech": "315909", "IWILL": "456711", "JABEES": "736443", "JABLUE": "1219369", "Jabra-Fake": "472922", "Jawbone": "338297", "Jelly Belly": "564143", "JPL": "339180", "Kanen": "524140", "Kaos": "514453", "Karade": "103754", "Kazimogo": "431918", "KEEKA": "829717", "KEEP OUT": "1034262", "Kit": "307232", "Kitmobile": "455698", "KLIM": "1255750", "Kondor": "224722", "KOTHAI": "686567", "kotion": "1156535", "KREAFUNK": "1156406", "KSIX": "725643", "Kworld": "325694", "Lanso": "402483", "LAPINETTE": "1171962", "Laura Technology": "455473", "LDNIO": "1020927", "Le Coq Sportif": "93237", "Leicke": "563949", "LEILING": "1166074", "Levi`s": "437566", "LG-FAKE": "495498", "LIBRATONE": "666669", "LIONCAST": "1019922", "Logic": "222845", "LOVELY@ME": "1199596", "LUCID SOUND": "1161559", "Luxa2": "548341", "Maas": "417926", "Mad Catz": "226140", "Maplin": "399815", "Marmitek": "270229", "MAROO": "693151", "MARS GAMING": "1117827", "Martin Logan": "291734", "MARVO": "664385", "Maxon": "93512", "Maxwise": "495986", "MCA": "339700", "M-Cab": "314784", "Meizu": "309564", "METERS MUSIC": "1231019", "MICROMOBILE": "770011", "MIIKEY": "753888", "Mini": "97174", "Mionix": "499718", "MIPOW": "667257", "Mipro": "276065", "Miq": "457074", "mitec": "756206", "Mitel": "270233", "Mitsubishi/Trium": "234845", "Mixcder": "1176422", "Mizoo": "1215104", "Mobil System": "103740", "Mobil Team": "103798", "Mobiland": "142724", "MOBILE TUNING": "1087202", "Mobilize": "567075", "Mobisys": "272529", "Mocca Design": "1047127", "Modelabs": "428953", "mojoburst": "1069025", "MOLAMI": "810762", "Momodesign": "427312", "MOOSTER": "670308", "More": "93711", "MORUL": "1084627", "MOSIDUN": "856706", "Mov": "328864", "MPOW": "1129376", "Ms-Tech": "287017", "MTE": "103769", "Mtek": "225778", "MTT": "324606", "MTU": "93741", "Multimedia": "220181", "MUSIC SOUND": "1256958", "mydoodah": "1037612", "My-Extra": "327740", "NACON": "1102763", "Naks": "302173", "Native Union": "573437", "Navroad": "434738", "NEKKER": "669239", "Nelyo": "571889", "Net Generation": "436182", "New Mobile": "545528", "Nextlink": "307471", "NOCS": "480564", "Noganet": "506105", "NOISEHUSH": "725857", "NOKIA MONSTER": "744537", "Nokia-Fake": "458169", "NOOSY": "1067131", "Novero": "545016", "Nox": "486846", "N'Play": "538930", "Nuance": "278831", "Nueboo": "1214301", "NUHEARA": "1235955", "NX One": "441396", "Nxzen": "440390", "Nyko": "226099", "NZUP": "902703", "OAC": "103751", "OBLANC": "829660", "Odoyo": "422506", "OGLO": "1189820", "Oke": "480912", "Omiz": "400307", "ONEDIRECT": "1271421", "Orange": "309505", "ORB": "524581", "ORIGINAL FAKE": "659156", "Ovc": "451281", "Ovislink": "220187", "Ovleng": "501077", "OYKON": "1185452", "Ozone": "228334", "Pama": "237233", "PATUOXUN": "1122017", "PC Line": "217567", "PDP": "458182", "Pearl": "94106", "Perixx": "434997", "Peter Jäckel": "286875", "Philo": "400463", "Phone Team": "317290", "Pine": "97360", "PK": "326021", "Plantronics": "94193", "Platinet": "323244", "play2Run": "1096716", "PLAYVISION": "1022616", "PLUGGED": "1256968", "PMR": "509736", "Pnx": "433862", "Point Kom": "267622", "POLEGAR": "839119", "Power A": "547366", "PowerCool": "521205", "Powerwalker": "433246", "PRECISION AUDIO": "1104093", "PREMIUMCORD": "1054838", "PRIF": "1161136", "Pritech": "452190", "PROJECT SUSTAIN": "808156", "Promate": "428654", "PRS": "1196241", "Pryma": "237238", "Pump Audio": "1210054", "QCY": "855275", "Qoltec": "596219", "Q-pad": "548376", "Q-Sonic": "234736", "Qtek": "290489", "Qtrek": "422164", "Qumo": "396341", "RDI": "103765", "Rebeltec": "1068838", "redlife": "1145732", "REMAX": "689117", "Retrophone": "416196", "Richter": "94513", "Right": "400723", "Rix": "499142", "Roc": "487084", "Roccat": "489889", "Rock": "231119", "Rocketfish": "521626", "Roman": "232412", "S BOX": "1081568", "SADES": "756259", "Salsa": "226111", "Samsonite": "94678", "Samsung-Fake": "472920", "Santok": "446916", "SATECHI": "626606", "SAVOX": "1075019", "SBE": "367156", "SBS": "145041", "SEAWAG": "1145132", "Seekas": "1203427", "Sempre": "495052", "Sena": "530400", "Sendo": "259653", "SENSO": "1155571", "Sep": "237305", "Setma Deltam": "103714", "SFR": "103731", "SGP": "682655", "Sharkoon": "295824", "SHOT CASE": "1229511", "SINJI": "1138718", "Sitecom": "260359", "Skech": "572144", "Skillkorp": "1229383", "SKYLANDERS": "814883", "Smart TALK": "1077982", "SMARTHAX": "1230206", "Snap": "234188", "Snom": "318108", "Sofare": "103721", "Somic": "326253", "Soncm": "453697", "Sonim": "438898", "SONIXX": "664293", "Sony Ericsson": "278299", "Sony Ericsson-Fake": "472916", "Sony-Fake": "495589", "SoundPEATS": "1229892", "Sounds": "401226", "SOUNDZ": "1230354", "Southwing": "316563", "Soyt": "441006", "Spark": "427789", "Sparkle": "267599", "SPARTAN GEAR": "1156988", "spectralink": "1040795", "SPIRIT OF GAMER": "1051789", "Sports": "222889", "Spydee": "499371", "Starline": "95069", "STEELPLAY": "1124392", "STK": "420656", "STORM7": "815207", "Strax": "298503", "SUDIO": "500776", "SUNEN": "865275", "SUPERDRY": "699426", "Supertooth": "317083", "SWISS CHARGER": "664179", "SWISS MOBILE": "1141791", "Swissvoice": "296139", "Syba": "496094", "SYSTEM-S": "1100844", "TALIUS": "722480", "Talk Aloud": "441291", "TAMTAM": "1039674", "TAOTRONICS": "1069402", "Techair": "307406", "Techmade": "421823", "Techsolo": "309060", "Techtools": "326422", "TEKNISER": "872548", "Tektos": "500453", "Tekuni": "292801", "Telcom": "309504", "Teppaz": "596181", "TESORO": "712836", "THB Bury": "95351", "The Kase": "1183308", "The Wand Company": "805809", "Thermaltake": "315389", "ThunderX3": "1184951", "TIKOO": "689228", "Tiptel": "95388", "Tonino Lamborghini": "1068551", "TOP": "95404", "Top Suxess": "103713", "Topcom": "95414", "Topp": "221003", "TOTU DESIGN": "1167004", "Trade Invaders": "1117824", "TRAINER": "1145086", "TRANDS": "1126175", "TRENDWOO": "1114211", "Tritton": "401661", "TTLIFE": "1203711", "Tucano": "260285", "Turtle Beach": "220203", "Twiins": "509358", "Twodots": "770795", "ubsound": "1078084", "UCALL": "838796", "UIISII": "1159659", "ultimate ears": "1024083", "Under Control": "509444", "Union": "97887", "Uniq": "1123220", "UNPLUG": "846694", "Urban Factory": "475943", "URBANISTA": "671739", "Us Blaster": "316432", "USAMS": "803788", "VAIN SOUND": "855795", "VENTION": "1156490", "Veova": "1205989", "Vespa": "599109", "VETTER": "1168023", "VICTSING": "1113875", "VIDVIE": "1192958", "Viji": "103781", "Viking": "143335", "VULTECH": "872936", "VXI": "329746", "Wantek": "1223846", "Wave": "270250", "Wave Concept": "1226690", "WAYTEX": "683088", "WEARHAUS": "1256837", "WESDAR": "1145840", "WHATEVERITTAKES": "750951", "White Diamonds": "611530", "Wiko": "599484", "WILEYFOX": "1151219", "WIRED-UP": "753689", "WOO": "744021", "WOOPSO": "659687", "Woozik": "1190131", "Woxeo": "436208", "WTT": "320767", "X2": "482552", "XCSOURCE": "1078175", "XD DESIGN": "745365", "XFX": "293638", "Xpower": "309420", "Xtech": "417954", "Xubix": "1023556", "YADA": "502011", "Yarden": "98022", "YAYAGO": "1026496", "Yealink": "418175", "Zaapa": "237273", "ZEALOT": "1068788", "Zedem": "416171", "Zickplay": "439414", "Zipper": "459225", "ZOOOK": "1107856", "ZOWIE": "543936", "Zucchetti": "320120", "Zykon": "141060", "3bon": "495266", "AC Ryan": "516139", "Actidata": "574401", "Adaptec": "90481", "A-Data": "301769", "Addion": "305682", "ADLINK": "803433", "Agestar": "549770", "Akitio": "611630", "Allnet": "220119", "Alps": "90608", "Amacom": "305501", "AMD": "139827", "ANACOMDA": "1191322", "ANGELBIRD": "1067038", "Apacer": "262974", "Apache": "260662", "Apricorn": "340087", "Areca": "569718", "Argosy": "220116", "ASUSTOR": "812412", "Axiom": "217801", "Barracuda Networks": "402560", "Beghelli": "290961", "BIDUL": "1020738", "BIPRA": "864807", "Biwin": "397183", "BLU-BASIC": "689430", "Blue Coat": "319095", "Bluemedia": "310996", "BOSTON": "1073608", "BRINELL": "626758", "Cables Direct": "318991", "CCTV": "1097410", "Check Point": "283554", "Chenbro": "315630", "Chieftec": "316873", "Clickfree": "484612", "Cloud": "290850", "CMS": "319643", "CnMemory": "318107", "Cometlabs": "262546", "CONNECTED DATA": "873901", "Connection": "292717", "Coskin": "324657", "CRU": "472727", "Crucial Technology": "297835", "Ctera": "1057235", "D&S": "231297", "DAHUA": "588927", "Dane Elec": "219992", "Data Direct Network": "311115", "DATALOCKER": "694285", "Dawicontrol": "499421", "DESTROY POP": "1086969", "Digittrade": "458095", "Disques Silice": "482457", "Dothill": "443998", "DROBO": "478930", "Durabook": "742470", "Easyraid": "308894", "Edimax": "269473", "Elgato": "316604", "EMC": "91871", "Energy": "109120", "Europart": "91973", "Exabyte": "311121", "Excelstor": "302905", "EXTERITY": "829040", "FUSiON-iO": "610205", "Geil": "398407", "Getac": "290263", "GOLD DIGITAL": "1173801", "Golden Memory": "1079185", "GOO": "1223194", "Goodram": "396347", "G-Technology": "96673", "HGST": "804142", "HI-LEVEL": "665620", "HipDisk": "1159231", "HITACHI DATA SYSTEMS": "669230", "HMB": "450562", "HORNETTEK": "589640", "Hyperdrive": "307549", "Hypertec": "220160", "I Storage": "435752", "I.NORYS": "1107446", "Icy Dock": "414949", "Imation": "103402", "Infortrend": "315426", "Innodisk": "398977", "Integral": "223966", "Iocell": "399007", "Iomega": "92836", "ioSafe": "565347", "Ironkey": "472516", "ISO": "229471", "Jou Jye": "329851", "Kanex": "606759", "Kanguru": "449020", "Kentron": "221382", "KFA2": "1163240", "King Elephant": "283007", "Kingmax": "220169", "KINGSPEC": "547649", "Kingston": "140804", "KLEVV": "1143492", "Level One": "220175", "Lexar": "143720", "Leyio": "528542", "Linksys": "271787", "LONGSYS": "864399", "Lorca": "263518", "Lupus": "423665", "Maxtor": "302904", "Mc Afee": "93520", "MDT": "431174", "ME2": "417854", "MediaRange": "437503", "Memblaze": "1140924", "Microcom": "93614", "Micron": "93619", "Micronet": "220280", "Microstorage": "321790", "Mitsumi": "93669", "Momobay": "305724", "Mophie": "443748", "Mpio": "261284", "Mtron": "475440", "Mushkin": "431175", "MX-Technology": "575640", "Nasdeluxe": "501962", "Netapp": "314890", "Newcom": "258420", "NewerTech": "600035", "Nexsan": "441439", "Nextodi": "495275", "NIMBLE STORAGE": "725037", "Novatech": "309444", "NOVATHINGS": "1264351", "Ocz": "427981", "One Technologies": "225300", "Onnto": "394142", "Origin Storage": "322063", "Overland Storage": "308893", "OWC": "693923", "PANASAS": "709544", "Patriot Memory": "595685", "Perfectparts": "805949", "Pexagon": "434314", "Pikaone": "297709", "Planet": "116425", "Platinum": "223310", "Plextor": "94206", "PNY Technologies": "219993", "Promise": "265112", "PURE STORAGE": "1073144", "QSAN TECHNOLOGY": "678278", "Quantum Corporation": "315447", "RAIDON": "548057", "Rapsody": "417947", "Riverbed": "545117", "Rixid": "428870", "RUBRIK": "1185143", "Runcore": "511674", "Sandisk": "139805", "Seagate": "94795", "Seitec": "303378", "Silicon Power": "321784", "Silicon Systems": "434436", "Simpletech": "294118", "SK hynix": "1045832", "Smartbuy": "261830", "Smartdisk": "290351", "SMC": "94925", "Snap Appliance": "314883", "SOLIDATA": "527431", "SOLIDFIRE": "1113858", "Sonicwall": "402564", "Sonnet": "271851", "SONNICS": "1040259", "SQP": "267494", "Stardom": "443577", "Startech": "97703", "sTec": "1077985", "Storeva": "512373", "Storevault": "482222", "StorVision": "421544", "STREACOM": "696314", "Sun Microsystems": "224842", "Super Talent": "325738", "Symantec": "95193", "Synology": "439154", "Tanya Sarne": "320343", "Teamgroup": "431180", "TERRAMASTER": "1067163", "THECUS": "444656", "TOP PERFORMANCE": "1164556", "Travel Star": "401653", "Trendnet": "283788", "TVTECH": "736434", "V7": "726127", "Vantec": "231970", "VCE": "846415", "Veritas": "435964", "Vosonic": "295895", "Welland": "95758", "Western Scientific": "315420", "WHIPTAIL": "749125", "Xerom": "418046", "Ximeta": "311044", "Xiotech": "599779", "X-Micro": "324583", "XPG": "1256896", "Xs Drive": "415493", "Xyratex": "315421", "Xystec": "460486", "ZAPPITI": "838767", "Zyxel": "95942", "Aaxa Technologies": "548785", "Acco": "224378", "Adapt": "431335", "A-Rival": "457820", "Ask Proxima": "502046", "Avio": "316466", "Beambox": "524333", "BLUECAT": "1206021", "Boxlight": "268470", "Christie": "309026", "CineVersum": "482456", "Crenova": "500030", "Davis": "139333", "Digital Projection": "403131", "Dream Vision": "149357", "Eiki": "103804", "Elmo": "149356", "E-Projex": "547129", "EVERLINE": "690118", "Fujix": "92226", "GOPICO": "1066186", "I3": "398926", "iCodis": "1209471", "INNOIO": "1255954", "IPOWERUP": "742569", "JmGO": "1207387", "Kindermann": "93043", "Liesegang": "93292", "LUXBURG": "1108206", "Luximagen": "1228996", "MediaLy": "1081827", "Microvision": "93625", "Mili": "597861", "Mimio": "806881", "Miroir": "1176137", "Nobo": "222853", "Optoma": "288341", "Phonica": "221499", "Puridea": "1167545", "RIF6": "1209633", "Runco": "268485", "SceneLights": "545809", "SHOPINNOV": "1064766", "Sim2": "291556", "SIMPLEBEAM": "1278778", "Starview": "455863", "Suant": "493753", "TECTECTEC": "1162509", "UHAPPY": "1088061", "Unic": "281790", "Unicview": "1224864", "WowWee": "509558", "XSAGON": "1073011", "Zte": "315405", "3Free": "567171", "808": "1100573", "8BITDO": "1159947", "A Dece Oasis": "1189767", "abit": "220107", "Aboutbatteries": "436565", "AC WORLDWIDE": "1175513", "Acoustic Energy": "259315", "Acoustic Research": "90457", "Addon": "327483", "AIBIMY": "1143517", "AKAI PROFESSIONAL": "1065781", "Akios": "481760", "ALILO": "842148", "ALLOCACOC": "1120929", "Altec": "429058", "AM-Denmark": "90613", "Amir": "231355", "Aml": "1159591", "Ansmann": "90646", "Aodasen": "482648", "Apart": "304885", "Aq": "328545", "AQ AUDIO": "667811", "AQUAJAM": "1088118", "Aquamusique": "448488", "Arkas": "365852", "Arowana": "96114", "Assmann": "90745", "ASWY": "1143006", "Atake": "396971", "Audica": "329451", "Audio Tech": "96143", "AUDIOBOT": "813293", "Audioengine": "565414", "AUDYSSEY": "682623", "Auluxe": "567291", "AUTODRIVE": "667590", "AV CONCEPT": "737881", "Avanti": "96157", "AVS": "549892", "Awg": "397036", "AZATOM": "864500", "BASS EGG": "1046493", "Beacon": "231139", "BEM": "855913", "Beqube": "402525", "BIJELA": "670416", "BINAURIC": "1097803", "Blautel": "592258", "BLEE": "1081297", "Boom": "225999", "BOOM BOTIX": "688351", "Born in France": "1207857", "BOUNCE AUDIO": "1166078", "Boynq": "435796", "BRAVEN": "749360", "B-SOUND": "1104095", "Bull Audio": "433125", "BUNKERBOUND": "671598", "Burger": "91176", "BUZZEBIZZ": "841153", "Cabasse": "91195", "Cambridge Soundworks": "283781", "CAMINO": "1182384", "CANNICE": "589335", "Canton": "91217", "CARBON AUDIO": "815180", "CaseGuru": "1048242", "Cellux": "229621", "Chaumet": "428373", "CHOIIX": "514985", "Cimline": "220081", "Cirkuit": "449035", "Cjc": "228266", "Cml": "316237", "Comep": "305882", "Computer Sound": "291805", "Conran Audio": "625226", "Coppertech": "1198996", "COUSOUND": "744517", "CRISTALRECORD": "671254", "Crono": "227090", "Crystal Speaker": "516059", "CUBELIGHT": "1117604", "CuboQ": "1159655", "Cuc": "227091", "Dali": "220507", "Dane Electronic": "545779", "DBEST": "687276", "D-Box": "220084", "Delux": "329826", "Dexlan": "319029", "Dexxa": "91593", "Diagram": "233950", "Diasonic": "293732", "DICE": "896937", "Digifocus": "445095", "Digital Inmotions Electronics": "494727", "DLH Energy": "421450", "Dmax Subtri": "293259", "Doss": "366593", "DOUPI": "1165319", "Dr. Bott": "272380", "DREAMWAVE": "1163107", "DRESZ": "739829", "DURALINE": "1105399", "D-VICE": "810785", "Dynaudio": "91749", "EARISE": "770849", "EasyAcc": "848800", "E-Boda": "339716", "ebode": "807085", "Eclipse": "140758", "ECOXGEAR": "865426", "Edtasonic": "220434", "Electric Friends": "611704", "Electrojoe": "544769", "Elite": "224767", "emie": "1069470", "EMOI": "690176", "en&is": "1096594", "EPIKO": "1145249", "Euro-10": "224398", "Ever Power": "490992", "Evestar": "521354", "Evidence Acoustics": "287930", "Ewoo": "501345", "Extel": "263180", "EZWAY": "674718", "F&d": "477711", "FADEDGE": "1125968", "Fantasia": "269583", "FASHIONATION": "499729", "Fatechs": "434812", "Fenton": "225471", "FINITE ELEMENTE": "659280", "Fizz": "507114", "Force Media": "598353", "Franklin Electronic Publishers": "304210", "Fred & Friends": "599458", "FUGOO": "1093804", "Fujitel": "323744", "FYDELITY": "712051", "Gameron": "436586", "Gamester": "226096", "GEAR HEAD": "744016", "GEAR IT": "770157", "GECHO": "1064410", "Gecko": "398406", "GIMME TUNES": "712332", "GLOBAL GIZMOS": "1127200", "Global Pad": "235567", "GO GROOVE": "1102041", "GO ROCK": "562682", "GOAL ZERO": "728436", "Good Vision": "338780", "GOODIES": "667965", "GRACE DIGITAL": "873902", "Grayt Little Speaker": "508198", "Grohe": "92411", "G-Series": "305455", "Guillemot": "92440", "GVC": "1069005", "HABY": "839196", "HCM": "92555", "HEADSOUND": "1128354", "Hiro Corporation": "482823", "Homade": "502956", "Hurricane": "431221", "iBass": "416886", "iBlock": "493809", "IBM/Lenovo": "414933", "IBomb": "1084134", "iBoutique": "856011", "ICE": "92739", "Ichona": "433453", "ICUTES": "838775", "Ik": "96864", "IKU": "1105796", "ILE": "1104761", "Imaingo": "449633", "IMIXID": "1122207", "In2uit": "1028982", "INCIDENCE": "724965", "Inkel": "116298", "Inno": "160432", "INNOVATEC": "687575", "INTENSE": "742114", "INVOXIA": "1114198", "iriver": "287457", "iRock": "1099149", "I-Rocks": "324623", "iSHOWER": "847578", "ISOTECH": "803491", "Istar": "399027", "Itamtam": "595180", "ITB Solution": "440062", "IUI": "687234", "Iwi": "282692", "Ixos": "232382", "JAMMIN PRO": "625948", "Jarre": "599001", "Jazz": "218214", "JBL Fake": "1192052", "JBLAB": "1104926", "Jnc": "314659", "JPW": "220085", "Juice": "502547", "Juster": "224474", "KAKKOII": "813214", "Kanto": "548053", "Kensington": "93017", "Klein und More": "574612", "K-Mex": "440486", "Koda": "272564", "Kores": "93118", "KRATOR": "519474", "Kt Tech.": "399482", "KUBXLAB": "1024450", "La Chaise Longue": "317855", "Lars & Ivan": "488309", "Laser": "103419", "Lecci": "571151", "Ledwood": "1200824", "Leitz": "93259", "Lemus": "1216841", "LENRUE": "696064", "LEPA": "625957", "LEPOW": "848401", "LICK": "1084321", "LIFEPROOF": "725199", "Lingo": "573966", "LINX": "1142695", "Linx": "219359", "LITTLEBIGSOUND": "731100", "Logicool": "399712", "Lonsen": "220086", "LOTS": "683960", "Luckies": "1057826", "LUMISKY": "1073754", "Luxy Star": "1060322", "Mac Audio": "93396", "Macrom": "97089", "MADISON": "1145104", "MAGIC CLOUDS": "1107672", "Maxi": "150354", "Maxview": "223436", "MEMORYSTAR": "711907", "MIGHTY BOOM BALL": "808178", "Miglia": "314849", "Mirage": "93656", "Miscella": "283774", "Mission": "93659", "MJS Technology": "476770", "Mobi": "322058", "MOBILITY ON BOARD": "1202107", "Mobinote": "393657", "MOCCA": "803463", "MONSTERCUBE": "1122394", "MOO": "1021465", "MOOAS": "1024655", "Morel": "93712", "MOVA": "472929", "MOVIO": "1084444", "MR & MRS FRAGRANCE": "815164", "Mt Logic": "160437", "Munchkin": "436193", "MUSAIC": "1184319", "MUSIBYTES": "687858", "Music angel": "499400", "MY AMP": "1097597", "My Music": "426099", "Nakamichi": "93777", "NEW THEORY": "1074646", "NILLKIN": "733818", "Nimzy": "432653", "Nippotec": "328897", "NJOY": "460901", "NOONDAY": "1102650", "Northamber": "447992", "NPN": "294151", "Nubwo": "617146", "NUDEAUDIO": "1023942", "NYNE": "1074644", "OAXIS": "686207", "Officedata": "93922", "OLIVARY": "1191854", "OMPERE": "811521", "ORA ÏTO": "1094056", "Orbitsound": "503356", "Origaudio": "742430", "OSMOT ECO-LIGHT": "673403", "PADMATE": "850611", "PALADONE": "445717", "Palo Alto": "339518", "Patrick": "94087", "Paul Frank": "436890", "Paulmann": "94095", "PEAQ": "595653", "PERIPOWER": "749277", "Philippi": "1078402", "Phonotonic": "1191893", "Pickering": "272834", "pindo": "1057178", "PIOU PIOU": "1034518", "PIXMI": "1129349", "PLOX": "1097951", "PLUFY": "990300", "Podgear": "338689", "Podspeakers": "428965", "POWERMOVE": "482234", "PowerTraveller": "420141", "Primax": "94281", "Pulse": "1211102", "Q Acoustics": "428447", "Qdos": "432733", "Qm": "94363", "Q-Tec": "225981", "RAIDFOX": "1044987", "Raikko": "539406", "Ranex": "270066", "Ravonaudio": "542814", "RAWAUDIO": "1207840", "Real Cable": "514863", "RED POSITIVE": "737167", "Re-Fuel": "1190085", "RIVA AUDIO": "1165077", "Rockfire": "94549", "Roth Audio": "442112", "ROXOBOX": "687846", "Saisho": "218023", "Scandyna": "400904", "Scythe": "471476", "SENGLED": "1108020", "SIMPLE AUDIO": "723851", "SIYOUR": "1164769", "SLIM PEARL": "1261064", "SMARTAKUS": "1232377", "sminno": "1164605", "Smk": "588627", "SMOOZ": "1179686", "SO SEVEN": "1127014", "Sonic Impact": "420638", "Sound Asleep": "611707", "Sound Traveller": "445641", "Soundcast": "458710", "SOUNDCRUSH": "1134131", "SOUNDLOGIC": "829719", "SOUNDS to go!": "869039", "Soundvision": "226548", "Soundyou": "600390", "Speakal": "524760", "Speck Products": "329272", "SPEEDMIND": "1027994", "Spherex": "338758", "Spire": "228356", "Spongebob": "415122", "SPRACHT": "754804", "Square": "415474", "SSBRIGHT": "1210288", "Stabo": "95043", "STELLE": "1084602", "Studio Lab": "259700", "Sub Zero": "222891", "Suck UK": "742499", "Sunflex": "95150", "SUPER LEGEND": "1084338", "Sveon": "515728", "SWISSTONE": "565453", "Tannoy": "95231", "TECNOSTYLE": "1060544", "Thakral": "366931", "Think Outside": "322072", "Thonet & Vander": "455525", "Titanmedia": "220221", "Tonality": "287453", "Tooq": "573693", "Topdevice": "456881", "TOPSAIL": "1190204", "TP-Link": "426433", "TRAIT TECH": "725083", "TREE-LABS": "1190508", "TSST": "547786", "TSU:BEHÖ:A": "1046482", "T-Visto": "437351", "Twelve South": "548340", "Twinmos": "292704", "TYLT": "1020774", "uBoogie": "521173", "ULTRALINK": "693572", "United Labels": "454999", "Unomat": "95557", "UP SOUND": "1184284", "Vers": "480346", "Vestalife": "496027", "VIBRA8": "547351", "VIBRASON": "801464", "Videologic": "97934", "Vifa": "217841", "VISION TOUCH": "1159163", "Vitalup": "436181", "VOCOCAL": "1151205", "Voix": "441005", "Wharfedale": "95786", "WHD": "97992", "WINK": "1108890", "Wowee": "607249", "WOWTHEM": "1095935", "WSTER": "800513", "XDREAM": "1044757", "XENICS": "549549", "Xindao": "504408", "Xonic": "367073", "XOOPAR": "570660", "Xtrem": "455037", "Ye!!": "833386", "Yuppi Love Tech": "1199438", "Zens": "478814", "Zeon": "218156", "Zignum": "428857", "ZOEETREE": "1278071", "ZOOKA": "811400", "AGURI": "1197444", "Amcor": "223564", "Audiovox": "103377", "Avmap": "319449", "Binatone": "91001", "Coyote": "549758", "Digma": "419985", "Domotix": "366353", "Dunlop": "263562", "ERLINYOU": "877078", "ESX": "96559", "Evensham": "339169", "Falk": "92034", "Geely": "812459", "Ifox": "502327", "IGN": "434433", "Kapsys": "499666", "Keomo": "415716", "Lowrance": "321172", "Magellan": "93415", "Magneti Marelli": "222738", "Mappy": "441574", "Memory-Map": "415003", "MGNav": "1172198", "Munic": "616474", "Myguide": "428395", "Navgear": "454378", "Naviflash": "324441", "Navigon": "224937", "Navking": "610241", "Navman": "272944", "Ndrive": "436838", "Norauto": "234375", "Novogo": "424094", "Overland": "219539", "Peiying": "436767", "REPLICA": "910723", "Route 66": "223697", "SILIM": "848833", "SKP": "226052", "Smailo": "504186", "Snooper": "223149", "Sungoo": "435126", "VDO Dayton": "114947", "Viamichelin": "311179", "VORDON": "1064880", "WIKANGO": "733288", "Witson": "1181864", "Xetec": "282799", "X-Loc": "431131", "X-Road": "457815", "Xzent": "475958", "Aone": "459112", "AtGames": "806969", "HYPERKIN": "1094928", "Ouya": "545366", "Sega": "94804", "SNK": "836811", "6MAX": "659379", "Altimea": "325786", "Amoi": "315012", "Arena": "454468", "Aspects": "305440", "ATMT": "416905", "Audix": "226425", "AUNE": "1093455", "Babysun": "516310", "Barthe": "103342", "Beat Sounds": "306004", "Bestlink": "338821", "Bluel": "301504", "BMS": "319599", "Bright": "91118", "Cayin": "149584", "Cebop": "284767", "Chic": "224389", "Cliod": "403104", "COLORFLY": "659278", "Dainet": "317430", "Deejay": "397754", "Diamond": "91599", "Digimania": "321835", "Digisette": "284580", "Digital Square": "288516", "Dolphin": "228280", "Dreameo": "422366", "EMATIC": "838915", "Emgeton": "274286", "ENMAC": "1261592", "Exigo": "393755", "Exper": "329843", "Ezav": "314415", "Finis": "500828", "Frontier Labs": "273026", "Genx": "310618", "Gweilo": "317458", "Hango": "265285", "HIDIZS": "1101812", "iAUDIO": "314438", "IKO": "440058", "Ingram": "321712", "Ioneit": "329977", "Iops": "317298", "Irok": "273004", "Ism Technologie": "301139", "Itronics": "480531", "Jazpiper": "233627", "KLIVER": "806476", "Lavod": "320809", "Live Music": "314837", "LOTOO": "1104240", "Magic Star": "291269", "Mambo X": "320810", "MARGOUN": "1105303", "Maxian": "339909", "Memory Power": "292312", "Microdia": "317108", "Mobiblu": "315407", "Mobilenote": "338439", "Monbeq": "338776", "Mpeye": "302923", "Muro": "314433", "Music Disk": "319043", "Muzio": "307499", "Mymemory": "338954", "Napa": "227879", "Netac": "235646", "New Tech": "113083", "Nextway": "308633", "Nomadeo": "302750", "Nomarque": "309724", "Nomatec": "329389", "Oasis": "222254", "Oracom": "305167", "Oricom": "303082", "Pacemaker": "495899", "Paxton": "309153", "Play on": "548313", "Pontis": "98980", "Pop3": "261759", "Powerman": "324521", "Questyle": "1162685", "RCA": "94431", "RIO": "271859", "Rownsonic": "403107", "Rox": "339425", "Saehan": "98981", "Saytes": "327130", "Selar": "403129", "Seltronic": "316782", "Shanling": "308626", "SHIK": "1133779", "Sonicblue": "260645", "Sylvania": "95192", "Synn": "310148", "Techmicro": "317046", "Tekeet": "521131", "Teknique": "223614", "TFD": "444001", "THE KUBE": "676841", "thebit": "1213168", "Unicom": "95533", "Vusys": "327929", "Wmg": "317102", "Woodi": "338347", "Xelo": "272073", "Xen": "316010", "Xpert": "402142", "Yves Fely": "1214251", "I-INN": "673389", "@TAB": "847792", "3Q": "515756", "4G Systems": "475955", "Ainol": "396764", "Aligator": "513449", "Allview": "339905", "ALPENTAB": "900165", "ALPIE TECHNOLOGY": "906249", "Apollo": "234931", "AQIPAD": "1080644", "ARNOVA": "669088", "ARRENA": "1073203", "ARTIZLEE": "1231661", "ArtView": "736241", "Barnes&Noble": "571041", "BAUNZ": "1024619", "Bebook": "547844", "BITMORE": "713107", "bq": "670310", "Cdip": "1051306", "CDISPLAY": "1085925", "Chicco": "259330", "Clarys Technolo": "1023016", "CLUST": "1020556", "Commax": "317266", "DF": "872890", "Dino": "96441", "DISCOVERY": "455236", "DPS": "682781", "Dyno": "414964", "EDERTIX": "1026133", "Einstein": "116294", "Eken": "597642", "ESTAR": "1093852", "E-STAR": "814907", "Evigroup": "609017", "Faktor Zwei": "460444", "FIREBRAND": "733452", "FONDI": "1061092", "FOODLE": "811670", "FORCEBOOK": "840755", "GOTAB": "729598", "HDW": "674552", "Hitek": "96817", "I.ONIK": "697763", "IGET": "865544", "Ikon": "583502", "Ikonia": "1069761", "INFINITON": "807068", "INNJOO": "1083114", "IONIK": "1157071", "Irbis": "307225", "IRULU": "736442", "Itel": "290832", "JMI": "810990", "Joyplus": "92927", "Ken Brown": "430681", "KLIPAD": "742548", "Kloner": "284769", "KOBO": "570358", "Konrow": "1105938", "Lark": "338802", "LOGIC-INSTRUMEN": "326057", "Magalhaes": "491645", "MID": "667608", "Multipix": "609261", "Myaudio": "441627", "MYMAGA": "1096060", "MYPAD": "664584", "Navon": "479659", "Nextbook": "607041", "No Name": "97245", "NOKIA (FI)": "1106740", "Nordmende": "93871", "NOVATAB": "869731", "NVIDIA": "1069044", "Nvsbl": "572016", "Onda": "308834", "ONYO": "626524", "Overmax": "476693", "Palit": "290220", "PANDIGITAL": "501409", "Papyre": "533470", "Phaser": "271961", "Pipo": "400492", "Pocketbook": "524639", "POSH": "671289", "POV": "847539", "Proscan": "268520", "QOOQ": "689953", "SKY-LABS": "697000", "SMARTAB": "1044651", "SMARTAK": "1231803", "Smartbook": "416160", "SQ": "668786", "Stanley Mobile": "1198494", "START TABLET": "805992", "Super General": "329343", "Synchro": "315739", "Szenio": "614216", "TB TOUCH": "1041498", "TECHNILINE": "853975", "Tecno": "217981", "Telecom": "97780", "TESLA": "1085941", "Texet": "218029", "tolino": "848807", "Tom-Tec": "338405", "TOO": "1065761", "TOUCHLET": "626574", "TOUGHSHIELD": "805176", "TURBOPAD": "753845", "ULTRA DIGITAL": "1036931", "Unowhy": "549761", "UNUSUAL": "1044858", "Vedia": "452820", "Versus": "436210", "Vexia": "499905", "Vido": "325693", "VINITY": "1037530", "VIRTUAL": "1047183", "Vodafone": "103763", "Wexler": "609371", "XIDO": "1145616", "Xplore": "325262", "X-treme": "503327", "ZENITHINK": "601832", "Zero": "95922", "ZIF": "1072690", "ZIPATO": "1073860", "Ardes": "267635", "Asel": "290416", "Bella": "290479", "Bielmeier": "285965", "CASINO DELICES": "755625", "Chang Sheng Electrical": "437050", "Chef Master Kitchen": "1155714", "COMFORTCOOK": "665360", "Cookworks": "223554", "Crafft": "232834", "CUSINIER DELUXE": "853511", "Doragrill": "294067", "DPE": "221474", "Durandal": "291262", "Elith": "521665", "Eltac": "398059", "Essential": "224471", "Forc": "231961", "Formido": "270059", "Galileo": "220439", "HOME ESSENTIALS": "1083452", "Home-Tek": "287759", "Kasui": "1200836", "Kdeo": "525969", "Kumtel": "288826", "Maister": "218521", "Newcook": "599606", "Roller/Grill": "230434", "SILVA HOMELINE": "847912", "Sirge": "288258", "Toyota": "222270", "Valory": "319063", "Vitrokitchen": "297617", "Vivalp": "95669", "Alpina": "439434", "Beer Supreme": "600038", "Bier Maxx": "425329", "Bier-Box": "524075", "Ezetil": "282822", "LA HOUBLONNIERE": "1155903", "Mobicool": "279429", "Multidraft": "503430", "Tireuse": "590868", "Wunderbar": "421608"};

  

  $scope.marcas_modelos_menu = {
    "marcas":[],
    "modelos":[]
  }

  $scope.marcas_modelos = {
    'TV_000':{

      'LG':[
         "55EG9A7V",
         "OLED65E7V",
         "OLED55B7V",
         "75UJ675V",
         "24MT49DF"
      ],


      'SAMSUNG':[
        "UE65MU9005",
        "QE55Q8C",
        "UE49MU6105",
        "UE75MU7005",
        "UE55MU9005"
      ],

      'PANASONIC':[
        "Viera TX-55EX600E",
        "Viera TX-50EX700E",
        "Viera TX-32ES600E",
        "Viera TX-40EX700E",
        "Viera TX-58DX750F"
      ],
      'SONY':[
        "Bravia KD-49XE7005",
        "Bravia KD-49XE7005",
        "Bravia KD-65XE7005",
        "FW-49XE9001",
        "Bravia KD-65XD7505"
      ],
      'PHILIPS':[
        "55PUS6262",
        "49PUS6551",
        "50PUS6162",
        "32PHS4112",
        "55PUS6551"
      ],
      'GRUNDIG':[
        "22VLE4520BF",
        "22 VLE 5520",
        "22VLE5520WG",
        "22VLE5520WG",
        "22VLE5520BG",
        "28VLE4500BF",
        "Vision 5 32 VLE 5503 BG",
        "32 VLE 417",
        "32 VLE 5503 BG",
        "32VLE6730BP",
        "28 VLE 5500",
        "Vision 6 32 VLE 6730 BP",
        "43 GFW 6628",
        "Vision 7 40 VLX 7730 BP",
        "40 VLE 7321",
        "Vision 7 49 VLX 7710 BP"
      ],
      'THOMSON':[
        "22FB3123",
        "32HD3101",
        "24 HA 4223",
        "22FB3113",
        "28HA3223",
        "28 HA 3223 W",
        "22FB3113",
        "32HC3121",
        "32HD3121",
        "32HD3121W",
        "40FB5426",
        "43UC6406",
        "43UC6306",
        "49UC6406",
        "43UC6406",
        "55UC6406"
      ]
  },

  //'LAVE_000':{
    
   // 'Aristo':[
   //   "AR",
    //  "AQ"
    //],
   // 'Asterie':[
   //   "AWM",
   //   "WM"
   // ],
   // 'Axane':[
   //   "ALS"
   // ],
   // 'Bellavita':[
   //   "LF",
   //   "LFT",
   //   "LFS"
   // ],
   // "Bendix": [
   //   "ML",
   //   "WLS",
   //   "BF"
   // ]

    // 'Whirlpool':[
    //         "AWOD070",
    //         "FSCR80421",
    //         "FSCR10432",
    //         "FSCR70421",
    //         "WWDP10716"
    //      ],
   
    //      'Electrolux':[
    //        "EWX127410W",
    //        "EWG127410W",
    //        "WE170P",
    //        "EWF1484",
    //        "EWF1284"
    //      ],
   
    //      'Samsung':[
    //        "WW12K8412OW",
    //        "WW90K5410UW",
    //        "WD80J5430AW",
    //        "WW70K5410UX",
    //        "WW80K6414QW"
    //      ],
    //      'Haier':[
    //        "HW100-BD14756",
    //        "HW80-B14636",
    //        "HW70-14829",
    //        "HW100-14636",
    //      ],
    //      'Candy':[
    //        "GC1472D",
    //        "Aqua 1041D1-S",
    //        "EVO 1683 DH",
    //        "AQUA 1142 D1",
    //        "AQUA 1042D1"
    //      ]
    // },

    'FRIGO_000':{
      'SAMSUNG':[
        "RF56J9040SR",
        "RSG5PUSL",
        "RB30J3000SAEF",
        "RB30J3000WWEF",
        "RS7547BHCSP "
      ],
      'HAIER':[
        "HRF-628IF6",
        "HRF-628AF6",
        "A3FE-742CMJ",
        "HB25FSSAAA",
        "B3FE742CMJW "
      ],
      'SMEG':[
        "FAB32LVN1",
        "FAB32LPN1",
        "FAB30LB1",
        "FAB32LBN1",
        "FAB32LAZN1"
      ],
      'SIEMENS':[
        "KD33EAI40",
        "KD33EAI40",
        "KA90DVI20",
        "KD46NVI20",
        "KI86VVS30"
      ],
      'BOSCH':[
        "KDV29VW31",
        "KID28V20FF",
        "KID26V21IE",
        "KIV34V21FF",
        "KGV58VL31S"
      ],
      'LIEBHERR':[
      "KTS 127",
      "T1400-20",
      "KTS 103",
      "GK 200",
      "KTS 103",
      ],
      'BEKO':[
      "SS137020",
      "BK7725",
      "BK 7725",
      "Refrigerateurs table top TS 190020",
      "TS190020 Blanc",
      ],
      'WHIRLPOOL':[
      "ARC 104 +",
      "ARC 104/1/A+ Blanc",
      "SW 6 AM 2 QW",
      "ARG 450/A+ Intégré",
      "ARG 750/A+ Intégré",
      ],
      'ELECTROLUX':[
      "ERN1300FOW Intégré",
      "ERT1601AOW3",
      "ERT1601AOW3 Blanc",
      "ERT1501FOW3",
      "ERT1501FOW3 Blanc",
      ],
      'KLARSTEIN':[
      "Big Picknicker",
      "Taverna Mini",
      "Picnicker XL Thermo",
      "Frosty",
      "17 L",
      ],
      'CANDY':[
      "Réfrigérateur compact CANDY - CFL050E",
      "CFL 050 E Blanc",
      "CFO 050 E Blanc",
      "CCTOS502",
      "CFL 050",
      ],
    },
    'FRIGO_001':{
      'SAMSUNG':[
        "RS7547BHCSP",
        "RS7687FHCSL",
        "RSG5PUMH",
        "RS7778FHCSL",
        "RS6178UGDSR "
      ],
      'HAIER':[
        "HRF-628IF6",
        "HRF-628AF6",
        "HRF-628IN6",
        "HRF-521DM6",
        "HRF-800DGS8"
      ],
      'SMEG':[
        "FQ60BPE",
        "FQ60NPE"
      ],
      'WHIRLPOOL':[
        "WSF 5574 A + NX",
        "WSC 5541 A+S",
        "WSG5588AM"
      ],
      'BOSCH':[
        "KAN92VI35",
        "KAD90VI30",
        "KAG90AI20",
        "KAD90VB20",
        "KAN58A55"
      ],
      'LIEBHERR':[
      "Liebherr SBSef 7242 Comfort",
      "SBSESF 7212 C",
      "SBSESF7212",
      "SBSES8663",
      "Liebherr SBSES 8663",
      ],
      'BEKO':[
      "RCSA 270 K 20 W",
      "RDSA240K20W Blanche",
      "RDSA 240 K",
      "CSA29020S Argent",
      "Beko RDSA310M20",
      ],
      'SIEMENS':[
      "KD29VVW30",
      "KD29VVW30 Blanche",
      "KD33VVW30 Blanche",
      "KI28DA20",
      "KG 33 NNL 30",
      ],
      'ELECTROLUX':[
      "EJ2801AOW2",
      "ERT 1502 FOW 3",
      "EJ 2803",
      "EJ1800AOW Blanche",
      "ERN 2011 FOW",
      ],
    },
    'FRIGO_002':{
      'WHIRLPOOL':[
        "WHM4611",
        "WHM2110",
        "AFB 828/A+",
        "WHM31112",
        "UW8 F2C XBI N "
      ],
      'BOSCH':[
        "GSN33VW31",
        "GSV33VW31",
        "GSN54AW30",
        "GID18A20",
        "GIN81AE30"
      ],
      'CANDY':[
        "CCTUS 542XH",
        "CCOUS 5142IWH",
        "CFU 050 E",
        "CCOUS 6172",
        "CCTUS 542"
      ],
      'BEKO':[
        "HS 210520",
        "HS 221520",
        "HSA40520",
        "RFNE312E33W",
        "HSA 32520"
      ],
      'SMEG':[
        "CVB20LNE1",
        "CVB20LP1",
        "CVB20RNE1",
        "CVB20RR1",
        "CVB20LR1"
      ],
      'LIEBHERR':[
      "GNSL2323",
      "GP 1213-20",
      "GX 823 20",
      "GP 1376 20",
      "GP 1476",
      ],
      'SIEMENS':[
       "GU15DA55 Intégré",
       "GI41NAC30 Intégré",
       "GI21VAD30 Intégré",
       "GI81NAC30 Intégré",
       "GS58NAW41 Blanc",
      ],
      'ELECTROLUX':[
      "Eub3002AOW",
      "EC2830AOW2 Blanc",
      "FFU19400",
      "Congélateur armoire Electrolux 933 012 728",
      "Congélateur armoire ELECTROLUX EUF2205AOW",
      ],
      'KLARSTEIN':[
      "10004086",
      "10029335",
      "Garfield XL Congélateur 4 étoiles 3 étages 75L 80W classe A+ - noir",
      "Iceblokk Congélateur 100 L 75 W classe A+ - blanc",
      "10029353",
      ],
    },
      'FRIGO_003':{
        'LA SOMMELIERE':[
          "TR2V121",
          "CVD102DZ",
          "LS50.2Z",
          "LS36A",
          "LS52A"
        ],
        'CLIMADIFF':[
          "VSV27",
          "CV41DZX",
          "CLS33A",
          "VSV12F",
          "VSV12F"
        ],
        'KLARSTEIN':[
          "Reserva Duett 12",
          "RESERVA PICOLA CLASS B",
          "Vinsider 35D",
          "Vinsider 24D",
          "Reserva Saloon"
        ],
        'LIEBHERR':[
        "WK 66",
        "WK137",
        "WKb 1812",
        "WKb 3212 Vinothek Noir",
        "WK 161"
        ],
        'CAVISS':[
        "SP16CFE",
        "SP118CFE",
        "SN130KBE4",
        "S148CBE4",
        "S149OBE3N"
        ],
        'AVINTAGE':[
        "AV 22",
        "AVU52SX",
        "AVU53CDZA",
        "DVA180G",
        "DVP180"
        ],
        

      },
      'TLF_000':{
        'SAMSUNG':[
          "Galaxy A3",
          "Galaxy S7",
          "Galaxy A5",
          "Galaxy S7 Edge",
          "Galaxy J7"
        ],
        'HUAWEI':[
          "Honor 6X",
          "P9 Lite",
          "P8 Lite",
          "Honor 7X",
          "Honor 6A"
        ],
        'APPLE':[
          "iPhone 5S",
          "iPhone 6",
          "iPhone 6 Plus",
          "iPhone 6S Plus",
          "iPhone 7",
          "iPhone 7 Plus"
        ],
        'ZTE':[
          "Axon 7 Mini",
          "Blade V8 Mini",
          "Nubia N2",
          "Axon 7",
          "Blade V8"
        ],
        'WIKO':[
          "Robby",
          "Riff 2",
          "View XL",
          "View Prime",
          "Freddy"
        ],
        'SONY':[
        "Xperia C",
        "Xperia J ST26i",
        "Xperia SP",
        "Xperia E4 noir débloqué",
        "Xperia M2"
        ],
        'MOTOROLA':[
        "DEFY MINI",
        "Fire XT316",
        "Moto E",
        "RAZR V3i",
        "Moto E3 Xt1700 Blanco"
        ],
        'NOKIA':[
        "C2 01",
        "105 Dual SIM",
        "105",
        "130",
        "2610"
        ],
        'HTC':[
        "Wildfire S",
        "DESIRE C",
        "Desire",
        "Touch 3G",
        "Explorer"
        ],
        'XIAOMI':[
        "Redmi 4A",
        "Redmi 5A - Double Sim - 16Go, 2Go Ram - Or",
        "Redmi 5A - Double Sim - 16Go, 2Go Ram - Gris Sombre",
        "Redmi Note 2",
        "Redmi 4X"
        ],
      },
      'COMPU_000':{
        'ASUS':[
          "VivoBook E200HA-FD0080TS",
          "VivoBook L402NA-GA042TS",
          "X540SA-XX311T",
          "VivoBook E200HA-FD0041TS",
          "Transformer 3 PRO (T303UA)"
        ],
        'APPLE':[
          "MacBook Air",
          "MacBook Pro",
          "MacBook Retina"
        ],
        'LENOVO':[
          "V510",
          "IdeaPad Miix 720-12IKB",
          "IdeaPad 710S-13ISK",
          "Miix 510",
          "Miix 510"
        ],
        'FUJITSU':[
          "Lifebook S781",
          "Lifebook T937",
          "Celsius H760",
          "Lifebook T901",
          "Lifebook E781"
        ],
        'HP':[
          "ProBook 440 G5",
          "ProBook 450 G5",
          "ProBook 440 G5",
          "ProBook 470 G5",
          "EliteBook 1040 G4"
        ],
        'ACER':[
        "Acer ASPIRE ES1-132-C3BM",
        "Acer Aspire A114-31-C8FD",
        "Acer Aspire A114-31-C5RN",
        "Aspire 1 A114-31-C4WM",
        "Acer SWIFT SF113-31-C74M",
        ],
        "MICROSOFT":[
        "Microsoft Surface Pro Core M 4Go 128Go",
        "12,3'' PixelSense",
        "Surface Laptop",
        "Tablette Surface Pro 4 Core M3",
        "Microsoft Surface Laptop i5 128go silver",
        ],
        'THOMSON':[
        "Thomson HERO 9",
        "NEO14-2.32BS",
        "THBK2-10.32CTW",
        "Hero 10",
        "Thomson NEO14-2WH32",
        ],
      },

      "c32001": {"Alcatel": [], "Bosch": [], "Brother": [], "BT": [], "Canon": [], "Citizen": [], "Crown": [], "Dell": [], "DeTeWe": [], "Develop": [], "Epson": [], "Fujitsu Siemens": [], "Gestetner": [], "Grundig": [], "HP": [], "IBM": [], "Infotec": [], "Jetfax": [], "Kodak": [], "Konica-Minolta": [], "KPN": [], "Kyocera": [], "Kyocera Mita": [], "Lanier": [], "Lexmark": [], "Medion": [], "Mita": [], "Muratec": [], "Nashuatec": [], "NEC": [], "OKI": [], "Olivetti": [], "Olympia": [], "Panasonic": [], "PANTUM": [], "Philips": [], "Pitney Bowes": [], "Plustek": [], "Rex Rotary": [], "Ricoh": [], "Sagem": [], "SAGEMCOM": [], "Samsung": [], "Sanyo": [], "Sharp": [], "Siemens": [], "Swisscom": [], "TA": [], "T-Com": [], "Toshiba": [], "Twen": [], "Utax": [], "Xerox": []},
      "c32022": {"AEG": [], "Airforce": [], "Airlux": [], "Altus": [], "Amica": [], "Apelson": [], "ARCOOK": [], "Ardo": [], "ARTHUR MARTIN": [], "Asko": [], "Atlantic": [], "Aya": [], "Balay": [], "Barazza": [], "Bauknecht": [], "Baumatic": [], "Beko": [], "Beldeko": [], "Bluesky": [], "Bomann": [], "Bompani": [], "Bora": [], "Boretti": [], "Brandt": [], "Broan": [], "BSK": [], "California": [], "Candy": [], "Carma": [], "Carrefour Home": [], "Cata": [], "Climadiff": [], "Coldis": [], "Constructa": [], "Continental Edison": [], "Cook Art": [], "Cooke & Lewis": [], "Curtiss": [], "De Dietrich": [], "Delonghi": [], "Doman": [], "Domeos": [], "Domino": [], "Dynor": [], "Edesa": [], "Electrolux": [], "Electrolux-Arthur Martin": [], "Electrum": [], "Elegance": [], "Elica": [], "ENO": [], "Esco": [], "Essentiel B": [], "EVERTON": [], "Exceline": [], "Fagor": [], "FAR": [], "Faure": [], "Finlux": [], "Firstline": [], "Foster": [], "Franger": [], "Franke": [], "fratelli onofri": [], "Frecam": [], "Friac": [], "Frionor": [], "Fulgor": [], "Funix": [], "GAGGENAU": [], "GE": [], "Glem": [], "Godin": [], "Gorenje": [], "Grossbill": [], "Haier": [], "Harrow": [], "HDC": [], "HDC Link": [], "High One": [], "Homer": [], "Hoover": [], "Horn": [], "Hotpoint": [], "Hotpoint-Ariston": [], "Hudson": [], "Hyundai": [], "IAR": [], "Iberna": [], "Ignis": [], "Ikea": [], "IKEA": [], "Indesit": [], "Jeken": [], "Jemko": [], "Junker": [], "Juno-Electrolux": [], "King": [], "King D'Home": [], "KitchenAid": [], "Kneissel": [], "Koch": [], "Kontact": [], "Kueppersbusch": [], "Kunz": [], "Kupper": [], "Kuppersberg": [], "La Germania": [], "Laco": [], "Laden": [], "Lago": [], "Lazer": [], "Leonard": [], "Liebherr": [], "LIMIT": [], "Link": [], "Linke": [], "Listo": [], "Luxhome": [], "Maison Valerie": [], "MANDINE": [], "Markling": [], "MATTHIS": [], "Matthis Induction": [], "Midea": [], "Miele": [], "Mondial": [], "Mtec": [], "Nardi": [], "NEFF": [], "NEMAXX": [], "Nodor": [], "Nogamatic": [], "NORD INOX": [], "Novidom": [], "Novy": [], "Oceanic": [], "Pelgrim": [], "Pitsos": [], "PKM": [], "Plus": [], "Presticook": [], "Privileg/Quelle": [], "Progress": [], "Proline": [], "Rommelsbacher": [], "Rosieres": [], "SAMANA": [], "Sancy": [], "Sauter": [], "Schaub-Lorenz": [], "Schneider": [], "Scholtes": [], "Scientific Labs": [], "Selecline": [], "Selection": [], "Sidex": [], "Signature": [], "Siltal": [], "Smalvic": [], "Smeg": [], "Sogelux": [], "Spider": [], "Star": [], "Steba": [], "Stoves": [], "Teba": [], "Technical": [], "Techwood": [], "Techyo": [], "Tecnolec": [], "Tecnolux": [], "Teka": [], "Telefunken": [], "Terim": [], "Thermor": [], "Thomson": [], "Triomph": [], "Unic Line": [], "Urania": [], "Valberg": [], "VENTE PRIVEE": [], "Vestel": [], "VIESTA": [], "Viva (Bsh)": [], "V-Zug": [], "Waltham": [], "Wells": [], "Weltco": [], "Westline": [], "Whirlpool": [], "White And Brown": [], "WMA": [], "Zanussi": [], "Zerowatt": []},
      "c32026": {"Akpo": [], "Alizee": [], "Allegro": [], "Alno": [], "Amsta": [], "Appliance": [], "Aspes": [], "Autogyre": [], "Axess": [], "Axiair": [], "B. Epoque": [], "BAUMATIC UK": [], "Bell": [], "Belling": [], "Berbel": [], "Bertazzoni": [], "Best": [], "BODNER & Mann": [], "Brandy Best": [], "Bricorama": [], "Castorama": [], "Corradi": [], "Cuisinella": [], "Curling": [], "Cylinda": [], "Designair": [], "Devel": [], "Dmo": [], "Domair": [], "Dometic": [], "Domo": [], "Ecg": [], "EDY": [], "Eico": [], "Ekoline": [], "Elcolux": [], "Elitair": [], "Eternal": [], "Etis": [], "Eureka": [], "Eurodomo": [], "Faber": [], "Fadis": [], "Falco": [], "Falcon": [], "Falmec": [], "FOX": [], "Francia": [], "Gutmann": [], "HBH": [], "Helkina": [], "Hygena": [], "Ices": [], "Igenix": [], "Ilve": [], "Innova": [], "Inter Gorenje": [], "Jet Air": [], "Klarstein": [], "Lacanche": [], "Ladywind": [], "Leisure": [], "Luxor": [], "Matfor": [], "Maya": [], "Mepamsa": [], "Metal": [], "Microligh": [], "Mobalpa": [], "Modulair": [], "New Air": [], "Oranier": [], "Pando": [], "Portinox": [], "Premiere": [], "Prima": [], "Rangemaster": [], "Recco": [], "Rectiligne": [], "Respekta": [], "Robin": [], "Roblin": [], "Sagoma": [], "Samac": [], "Samba": [], "Schmidt": [], "Sideme": [], "Silverline": [], "Technoline": [], "Technolux": [], "Tecnogas": [], "Tecnowind": [], "Tekma": [], "Tekno": [], "Tonda": [], "Turbo": [], "Turboair": [], "Unelvent": [], "URBAN": [], "Venmar": [], "Ventolux": [], "Victory": [], "Viva": [], "Vortice": [], "White Westinghouse": [], "Wild": [], "Windsor": [], "Zirtal": []},
      "c32310": {"Acorn": [], "Advent": [], "Agfa": [], "Agfaphoto": [], "Aigo": [], "Aiptek": [], "Airis": [], "Aito": [], "Akor": [], "Amstrad": [], "Aosta": [], "Apple": [], "Archos": [], "Argus": [], "Atipix": [], "Atlantis-Land": [], "AUTOGRAPHER": [], "Avant": [], "Benq": [], "Bluetech": [], "Braun Germany": [], "Bravus": [], "Bresser": [], "BRINNO": [], "BTC": [], "Bushnell": [], "CAMSPORTS": [], "Canal Toy's": [], "Carrefour": [], "Casa": [], "Casio": [], "CCam": [], "CEL-TEC": [], "Che-Ez": [], "Chinon": [], "Clipsonic": [], "Cobra": [], "Conceptronic": [], "Concord": [], "Connectix": [], "Contax": [], "Cool-Icam": [], "CORDEX": [], "Crayola": [], "Creative": [], "CYBER EXPRESS ELECTRONICS": [], "Cyberhome": [], "Darling": [], "Denver": [], "Digimaster": [], "Digital & Perspective": [], "Digital Blue": [], "Digital Concepts": [], "Digital Dream": [], "Digitrex": [], "Disney": [], "DNT": [], "Doerr": [], "Dxg": [], "DXO": [], "Easypix": [], "Eden": [], "Emprex": [], "Energy Sistem": [], "Ergo": [], "Exakta": [], "Ferrania": [], "Fisher-Price": [], "Fujifilm": [], "Fuuvi": [], "Gelcom": [], "Genius": [], "Giochi Preziosi": [], "Gopro": [], "Hasbro": [], "Hasselblad": [], "Hello Kitty": [], "Hercules": [], "Hitachi": [], "Hunter": [], "Imc": [], "Ingo": [], "Inovalley": [], "Instar": [], "Intel®": [], "Intova": [], "ION": [], "It Works": [], "I-Think": [], "IZYTRONIC": [], "Jaga": [], "Jay-Tech": [], "Jenoptik": [], "JVC": [], "Keystone": [], "KIDZ CAM": [], "Kobishi": [], "Kocom": [], "Koenig": [], "Konica": [], "KRIONIX": [], "Krypton": [], "Labtec": [], "Leica": [], "Lenco": [], "Lexibook": [], "Little Tikes": [], "LKM": [], "Logitech": [], "LTL ACORN": [], "Lumicron": [], "Luxya": [], "LYTRO": [], "Maginon": [], "Magpix": [], "MAPTAQ": [], "Mattel": [], "Maxell": [], "Mecer": [], "Media-Tech": [], "Mercury": [], "Minolta": [], "Minox": [], "Mistral": [], "MONSTER HIGH": [], "MPman": [], "Mustek": [], "Mystral": [], "NARRATIVE": [], "Nashita": [], "NCTECH": [], "Neo": [], "Neom": [], "Neoxeo": [], "Nexicam": [], "NGS": [], "Nikon": [], "NK": [], "Nomatica": [], "Nortek": [], "Novadia": [], "Novatek": [], "Odys": [], "Olympus": [], "Omisys": [], "Oregon Scientific": [], "OUAPS": [], "OVERLOOK": [], "Packard Bell": [], "Palm": [], "Peekton": [], "Pen Drive": [], "Pentagram": [], "Pentax": [], "PhaseOne": [], "PIVOTHEAD": [], "Pixturize": [], "Plawa": [], "Playskool": [], "Pnj": [], "Polaroid": [], "POWERSHOVEL": [], "Praktica": [], "Premier": [], "Pretec": [], "Prolink": [], "Pxor": [], "Pyle": [], "QPS": [], "Q-Ware": [], "Reflecta": [], "Reflex": [], "Relisys": [], "Rik & Rok": [], "Rimax": [], "Rollei": [], "Sakar": [], "Sampo": [], "Sangha": [], "Sanrio": [], "Scott": [], "Sealife": [], "Shiro": [], "Sigma": [], "Sigmatek": [], "Silverlit": [], "Sipix": [], "Skanhex": [], "Smart": [], "Smoby": [], "Sony": [], "Soundstar": [], "Soundwave": [], "Speedo": [], "Spin Master": [], "Spypoint": [], "Starblitz": [], "Stealth": [], "SUPERHEADZ": [], "Swann": [], "Sweex": [], "SWIMMING FLY SO": [], "Targa": [], "Tasco": [], "Techmobility": [], "Technaxx": [], "TECHTRAINING": [], "Teknofun": [], "Terratec": [], "Thompson": [], "Thumbs Up": [], "T'NB": [], "Tokiwa": [], "Trevi": [], "Trust": [], "Typhoon": [], "U": [], "Ultrasport": [], "Umax": [], "UNOTEC": [], "VD-Tech": [], "Vea": [], "VEO": [], "Verbatim": [], "Videojet": [], "Vista Quest": [], "Vitech": [], "Vivitar": [], "Vtech": [], "Waitec": [], "Werlisa": [], "Worldsat": [], "Yakumo": [], "Yamada": [], "Yashica": [], "YONIS": [], "Yoo Digital": [], "Yukai": [], "zstar": []},
      "c32506": {"AC-HOME": [], "Acm": [], "ACOPINO": [], "Addex": [], "Adler": [], "ADNAUTO": [], "AFK": [], "Aitek": [], "AKA": [], "Akiba": [], "Alessi": [], "Alfa": [], "ALINEA": [], "All Ride": [], "Altilux": [], "Amadis": [], "Amazon Basics": [], "Ariete": [], "Aroma": [], "Arzum": [], "Ascaso": [], "Astoria": [], "Auchan": [], "Avilla": [], "Barista": [], "Bartscher": [], "Beem": [], "Bella Professional": [], "Bellux": [], "Belmio": [], "BELMOCA": [], "Beper": [], "Bestron": [], "Betron": [], "Bialetti": [], "Bien Vu": [], "BLACK PEAR": [], "Black&Decker": [], "Blaupunkt": [], "Bluebell": [], "Bob Home": [], "Bodum": [], "BONAMAT": [], "Braun": [], "Breville": [], "Briel": [], "Brothers Choice": [], "Bugatti": [], "Butler": [], "C3": [], "Cads": [], "Caf": [], "Calor": [], "Camry": [], "Carpoint": [], "Carrefour Discount": [], "Casino": [], "Caso": [], "CASSELIN": [], "Chefn": [], "CHEMEX": [], "Chromex": [], "Cilio": [], "Cimbali": [], "Clatronic": [], "Cleveland": [], "Cloer": [], "Coffee Boy": [], "Coffee Cream": [], "Coffee Maxx": [], "Comi": [], "Conrad": [], "Convivium": [], "COSYLIFE": [], "CREMESSO": [], "Crena": [], "Crousti Light": [], "Cuisinart": [], "Cuisinier": [], "Cuisitech": [], "Cyclone": [], "Daewoo": [], "Dellar": [], "Delta Q": [], "Denwa": [], "DIDIESSE": [], "Domedia": [], "Domena": [], "Domoclip": [], "Drink Maxx": [], "D-tech": [], "Dualit": [], "Dyras": [], "E.ZICOM": [], "ECM": [], "Eco+": [], "ECODE": [], "Ecron": [], "Eculina": [], "Efbe-Schott": [], "Elcotec": [], "Electric Co.": [], "Electronia": [], "Elektra / Tradebrand Kruidvat": [], "Elsay": [], "Elta": [], "Emerio": [], "Emide": [], "Entronic": [], "Europa Style": [], "Eurotech": [], "Evatronic": [], "Everglades": [], "Exido": [], "Faema": [], "Fakir": [], "Figui": [], "First Austria": [], "Form+Funktion": [], "FrancisFrancis!": [], "Frifri": [], "G3Ferrari": [], "Gaggia": [], "Gastroback": [], "GAT": [], "Girmi": [], "Glenan": [], "Gotech": [], "Gourmet Maxx": [], "GPS ROUTE": [], "Graef": [], "GRAFNER": [], "Grossag": [], "Guzzini": [], "H.KOENIG": [], "HABITEX": [], "Hamilton Beach": [], "Handpresso": [], "Harper": [], "Hema": [], "Heru": [], "HOBERG": [], "Homday": [], "Hometech": [], "Ideeo": [], "Illy": [], "Inventum": [], "ITT": [], "J&R": [], "Jata": [], "JETTECH": [], "Jocca": [], "Jura": [], "Kaisui": [], "Kalije": [], "Kalorik": [], "Karcher": [], "KEM": [], "Kenwood": [], "K-Fee": [], "Kiovea": [], "Kitchen Chef": [], "Koala": [], "KOENIG": [], "Kooper": [], "Korona": [], "Krea": [], "Krups": [], "La Cimbali": [], "La Pavoni": [], "La Piccola": [], "Lacor": [], "Lagrange": [], "Laguiole": [], "Lamarque": [], "Lampa": [], "Lavazza": [], "Legal": [], "LELIT": [], "Lentz": [], "Leysieffer Kaffee": [], "Ligne Chrome": [], "Liventa": [], "LUCAFFE": [], "Lulu Castagnette": [], "Lysitea": [], "Maestro": [], "Magefesa": [], "Magimix": [], "Makita": [], "Malongo": [], "MANTA": [], "Martello": [], "Matea": [], "Max Italia": [], "Md": [], "Melitta": [], "Menage": [], "Mesko": [], "MIA": [], "Micromax": [], "Midland": [], "MINI MOKA": [], "MNI": [], "Moka": [], "Monix": [], "Morphy Richards": [], "Morris": [], "Moulinex": [], "M-Tec": [], "Mulex": [], "Mx Onda": [], "Myria": [], "Naelia": [], "Nemox": [], "Nescafe": [], "Nespresso": [], "Nesta": [], "Nestle": [], "Neufunk": [], "Nevir": [], "New Pol": [], "Nivona": [], "NORDIC HOME CULTURE": [], "Nova": [], "Nuova Simonelli": [], "Obh Nordica": [], "Orbegozo": [], "Orima": [], "Orva": [], "Oster": [], "OURSSON": [], "Palson": [], "Pavoni": [], "Peak": [], "PEM": [], "Petra": [], "Polti": [], "Powertec Kitchen": [], "Prim'Truck": [], "Princess": [], "Prinston": [], "PROFICOOK": [], "QBO": [], "QILIVE": [], "Quigg": [], "Rancilio": [], "Raydan": [], "Revelys": [], "Ritter": [], "Riviera": [], "Riviera & Bar": [], "Roadstar": [], "Robusta": [], "Rombouts": [], "Romix": [], "Rowenta": [], "RUN": [], "Russell Hobbs": [], "Saba": [], "Saeco": [], "Salco": [], "Salton": [], "Sapir": [], "Saro": [], "Scarlett": [], "Seaway": [], "SEB": [], "Segafredo": [], "Sencor": [], "Sensio": [], "SENYA": [], "Servitech": [], "Severin": [], "Silver Style": [], "SilverCrest": [], "Simac": [], "Simeo": [], "SIMPLY": [], "Sinbo": [], "Singer": [], "Siplec": [], "SMARTER": [], "Sogo": [], "Solac": [], "Solis": [], "Spd`Line": [], "Spidem": [], "Starway": [], "Suntec": [], "SUNTEC WELLNESS": [], "Support Plus": [], "Swan": [], "Swisstech": [], "Symex": [], "Taurens": [], "Taurus": [], "Tchibo": [], "Teacof": [], "Team": [], "Technivorm": [], "Techno": [], "Techno Diffusion": [], "Techno Sangoo": [], "Technomax": [], "Technostar": [], "TEESA": [], "Tefal": [], "Termozeta": [], "THE KITCHENETTE": [], "TM Electron": [], "Top Budget": [], "TOP CHEF": [], "Tous Les Jours": [], "Tower": [], "Trendy": [], "Trion": [], "Trisa": [], "Tristar": [], "Turmix": [], "TV DAS ORIGINAL": [], "Ufesa": [], "ULTRATEC": [], "Unold": [], "VENGA": [], "Vibell": [], "Viceversa": [], "Villaware": [], "Virages": [], "Viscio Trading": [], "Waeco": [], "Waves": [], "Wellness & Care": [], "Westwood": [], "WIK": [], "Wilden": [], "Winkel": [], "Winny": [], "WMF": [], "Zelmer": [], "Zephir": [], "Zomix": []},
      "c32512": {"Apell": [], "Aquaceane": [], "Ardem": [], "Artic": [], "Blomberg": [], "Bravo": [], "Carad": [], "Clayton": [], "Climaspace": [], "Edson": [], "Exquisit": [], "Favorit": [], "Frigistar": [], "Galanz": [], "HEC": [], "INEXIVE": [], "Jpc": [], "LG": [], "Linetech": [], "Manhattan": [], "Maytag": [], "Minea": [], "Ocean": [], "ORIGANE OLF": [], "Ormond": [], "OXFORD": [], "Radiola": [], "Schauen": [], "SE Electronic": [], "Servis": [], "Surfline": [], "Tucson": [], "Vedette": [], "Wellton": [], "Wesder": [], "Whitewash": [], "Witewash": [], "Xper": []},
      "c32516": {"Altic": [], "Aristo": [], "Asterie": [], "Ava": [], "Axane": [], "Bellavita": [], "Bendix": [], "Bluewind": [], "Boreal": [], "Calex": [], "Comfee": [], "Dawlance": [], "Deawoo": [], "Dyson": [], "Elvita": [], "Eudora": [], "Eumenia": [], "Faraon": [], "Frigidaire": [], "Galant": [], "Hemmermann": [], "Hightec": [], "Hisense": [], "Hohl": [], "JPC": [], "Kenmore": [], "La Redoute": [], "Lindbergh": [], "Master Chef": [], "Mastercook": [], "MEA": [], "MUBARIK": [], "ONECONCEPT": [], "Otsein-Hoover": [], "Perfekt": [], "Philco": [], "Polar": [], "Record": [], "Renlig": [], "San Giorgio": [], "Sedif": [], "SEG": [], "Siera": [], "Vendome": [], "VON HOTPOINT": [], "Wellington": []},
      "c32519": {"Atlus": [], "Creda": [], "DANUBE": [], "Falda": [], "GENERISS": [], "Ipso": [], "Kerwave": [], "Konrad": [], "LACASA": [], "MERKER": [], "Thomas": [], "White Knight": []},
      "c32521": {"Acctim": [], "ADIN": [], "Agashi": [], "Aiwa": [], "Akai": [], "Akira": [], "Akura": [], "Alba": [], "Albrecht": [], "Altec Lansing": [], "Amethyst": [], "Arelec": [], "Art Sound": [], "Artech": [], "Astone": [], "ATYLIA": [], "Audio Box": [], "Audio Pro": [], "AudioAffairs": [], "AUDIOCORE": [], "Audiola": [], "Audiopole": [], "Audiosonic": [], "August": [], "Auna": [], "AVENGERS": [], "AVENZO": [], "aves": [], "Avox": [], "Awa": [], "Axion": [], "Axxion": [], "B & O": [], "Balance": [], "Barbie": [], "Basicxl": [], "Batman": [], "BAYAN AUDIO": [], "Be": [], "BE MIX": [], "Bernstein": [], "BIG W": [], "BigBen Interactive": [], "Biostek": [], "BLACK PANTHER C": [], "Blow": [], "Bluestork": [], "Bml": [], "Boombox": [], "Boomstar": [], "Boost": [], "Bose": [], "Boston Acoustics": [], "Brionvega": [], "Brondi": [], "BTS": [], "Bush": [], "Caliber": [], "Cambridge Audio": [], "Casung": [], "Centurion": [], "CGV": [], "Clint": [], "CMP": [], "CMX": [], "Coby": [], "Com-One": [], "Connect Research": [], "Cotech": [], "Cresta": [], "Crony": [], "Crosley": [], "Crystal": [], "Cube": [], "CURVE": [], "Cygnett": [], "Day-Break": [], "Dcybel": [], "Delcom": [], "Denca": [], "Denko": [], "Denon": [], "Derens": [], "Dewalt": [], "DEXFORD": [], "Dieci": [], "DIGIVOLT": [], "DISUN": [], "DITALIO": [], "Divoom": [], "DJ-BOX": [], "D-Jix": [], "drobak": [], "Dual": [], "Durabrand": [], "DURONIC": [], "Dust": [], "DYNABASS": [], "Dynavox": [], "Dyon": [], "Ea2": [], "Easy Touch": [], "Edenwood": [], "Edifier": [], "Ednet": [], "Einhell": [], "EKIDS": [], "Elbe": [], "ELECITI": [], "Eltax": [], "Eltra": [], "Emerson": [], "Engel": [], "Engel Axil": [], "Epok": [], "Esperanza": [], "Eton": [], "Etsuko": [], "Eurocom": [], "Europsonic": [], "Evergold": [], "Evidence": [], "ezGear": [], "Fenner": [], "Ferguson": [], "FINESOUND": [], "FIVESTAR": [], "Flint": [], "FM": [], "Forever": [], "FPE": [], "Freecom": [], "Freeplay": [], "Fresh L.": [], "Fusion": [], "Fuxinko": [], "Gear4": [], "Geepas": [], "Gemex": [], "Gemini": [], "Geneva": [], "Global Sphere": [], "Goclever": [], "GOLD STAR": [], "Goldstar": [], "Goodmans": [], "GPO": [], "Grandin": [], "Griffin": [], "Gulli": [], "H&B": [], "Hama": [], "Hannspree": [], "Hardel": [], "Hdigit": [], "Heden": [], "Hisawa": [], "HOE": [], "Hoher": [], "Homedics": [], "Homemix": [], "HQ": [], "HT": [], "Hypson": [], "IBIZA SOUND": [], "I-CAPTURE": [], "Iconbit": [], "Icy Box": [], "IDANCE": [], "IDT": [], "Ifun": [], "iHome": [], "I-JOY": [], "Ilive": [], "Iluv": [], "Imagina": [], "Imperial": [], "INKI": [], "Inovaxion": [], "Intempo": [], "Intenso": [], "International": [], "Intersound": [], "I-Random": [], "IRC": [], "Irox": [], "Irradio": [], "IRT": [], "Jamo": [], "JBL": [], "Karma": [], "Kasuga": [], "KENGTECH": [], "Kenwin": [], "Kerzo": [], "Khorus": [], "Kitsound": [], "Klervox": [], "Kooky": [], "KOOL.STAR": [], "KRUGER & MATZ": [], "Kwai": [], "kwmobile": [], "Lacrosse Technology": [], "LAMAX": [], "Lansay": [], "Lasonic": [], "Lauson": [], "Leclerc": [], "Lecsound": [], "LEGAMI": [], "Lego": [], "Leotec": [], "LeSenz": [], "Lexon": [], "Lextronix": [], "Lloytron": [], "Logic 3": [], "Logik": [], "Logilink": [], "Lotronic": [], "lovemytime": [], "Lowry": [], "Ltc": [], "Macally": [], "Madcow": [], "Madison": [], "Magic Box": [], "Magnum": [], "Majestic": [], "Manesth": [], "Manta": [], "MAQ": [], "Mark": [], "Marquant": [], "Mate Star": [], "Matsui": [], "MAWASHI": [], "mayhem": [], "MBC": [], "Memorex": [], "Metabo": [], "Metronic": [], "Microlab": [], "Milwaukee": [], "Mitsai": [], "Mobility Lab": [], "Monitor Audio": [], "Monoprix": [], "Monster": [], "Motorola": [], "Moxie": [], "MR.WONDERFUL": [], "Msonic": [], "MTK": [], "Muse": [], "MUSKY": [], "Muvid": [], "MY DEEJAY": [], "Naf Naf": [], "Naiko": [], "Nanda Home": [], "National Geographic": [], "NES": [], "Nesx": [], "New One": [], "Nikkei": [], "Nilox": [], "NIZHI": [], "Nostalgic": [], "Novis": [], "Noxon": [], "Odeon": [], "Okano": [], "Omega": [], "ON.EARZ": [], "Ondex": [], "ONE by SEG": [], "ONE PLUS": [], "Onn": [], "Optimag": [], "Orion": [], "Orium": [], "Oshiwa": [], "Oxx": [], "OXX Digital": [], "Oxygen": [], "Ozaki": [], "Pacific": [], "Paris Saint-Ger": [], "Parrot": [], "Party Light&Sound": [], "Peha": [], "PERFECTPRO": [], "Philips Nike": [], "Pinell": [], "Pioneer": [], "PLATYNE": [], "Plustron": [], "Pointer": [], "Pollyflame": [], "Pop": [], "POSS": [], "POWERplus": [], "Prestige": [], "Prestigio": [], "Pro Basic": [], "Professor": [], "Profitec": [], "PROLINE AR": [], "PROSMART": [], "Prostar": [], "PRUNUS": [], "psyc": [], "Pure": [], "Pure Acoustics": [], "Q2": [], "QOOPRO": [], "QUBE": [], "Quer": [], "R.O.GNT": [], "Radialva": [], "Radiotone": [], "Reflexion": [], "Renkforce": [], "Revo": [], "Ricatech": [], "Ricco": [], "Roberts": [], "Rowa": [], "Rueducommerce": [], "Ryobi": [], "S&D": [], "S.DIGITAL": [], "S2 Digital": [], "Sailor": [], "Saisonic": [], "Salora": [], "Sangean": [], "Sansui": [], "SARDINE": [], "Satzuma": [], "Scansonic": [], "Schneider/TCL": [], "Schwaiger": [], "SDI": [], "SDIGITAL": [], "Sedea": [], "Shark": [], "Silva Schneider": [], "Skymaster": [], "Skytec": [], "Socrimex": [], "Sonoro": [], "SOULRA": [], "Sound Tech": [], "SOUND2GO": [], "Soundfreaq": [], "Soundmaster": [], "Soundmax": [], "SPC Telecom": [], "Spiderman": [], "Spirit": [], "Spirit of St. Louis": [], "Stanley": [], "Star Wars": [], "Steepletone": [], "Steljes Audio": [], "STEREOBOOMM": [], "Storex": [], "Strong": [], "Subsonic": [], "Sunfield": [], "Sunkai": [], "Sunstech": [], "Supertech": [], "Supra": [], "Sytech": [], "Tacens": [], "Takara": [], "Tamashi": [], "Tangent": [], "Target": [], "TCM": [], "TDK": [], "Teac": [], "TECHLY": [], "Technisat": [], "Tecsun": [], "Ted Baker": [], "Telemax": [], "Telestar": [], "Tellur": [], "Tensai": [], "Teufel": [], "TFA": [], "THALASSA": [], "Tivoli": [], "Tivoli Audio": [], "TIWIGI": [], "Tokai": [], "Toolland": [], "Tunbow": [], "United": [], "Vakoss": [], "Venturer": [], "Vibe": [], "Vibe-Tribe": [], "Vieta": [], "Viewquest": [], "Vita Audio": [], "VOV": [], "VQ": [], "VTIN": [], "VXR": [], "Walkvision": [], "Watson": [], "We": [], "Witti": [], "Woxter": [], "X4-Tech": [], "X-mini": [], "Xoro": [], "Xtreme": [], "Xtrememac": [], "Yamaha": [], "Yoko": [], "Yorx": [], "Zipy": [], "Zoetac": []},
      "c32533": {"Ab": [], "Absat": [], "ADB": [], "ADT": [], "Alcad": [], "Aldes": [], "Allsat": [], "Allvision": [], "Alma": [], "Amiko": [], "Amitronica": [], "AMTC": [], "Anttron": [], "APM": [], "Artec": [], "Aston": [], "Astrell": [], "Asus": [], "ATEMIO": [], "Atevio": [], "Atlanta": [], "ATLAS": [], "Atsky": [], "Aurex": [], "Auvisio": [], "Avanit": [], "Avermedia": [], "Axas": [], "Axil": [], "Axitronic": [], "Azbox": [], "Balmet": [], "Belson": [], "BEST BUY": [], "Bigsat": [], "BXL": [], "Cablecom": [], "CABLETECH": [], "CAHORS": [], "Canal Digital": [], "Canal Plus": [], "Canal Satelite": [], "Captimax": [], "Cherokee": [], "Chili": [], "CityCom": [], "CM3": [], "Colombus": [], "Columbia": [], "Columbus": [], "Comag": [], "Cosat": [], "Cristor": [], "CRT": [], "Cubsat": [], "CYBEST": [], "D2 Diffusion": [], "Dak": [], "Devolo": [], "Digiality": [], "Digihome": [], "Digilogic": [], "Digiquest": [], "Digitalbox": [], "Digitek": [], "Digitronic": [], "Disch": [], "Discovery": [], "Distra": [], "Distratel": [], "Distribat": [], "Distrisat": [], "Division": [], "Dream": [], "Dreambox": [], "Dse": [], "DTSAT": [], "Dune": [], "Dvico": [], "Easy One": [], "ECHOSAT": [], "Echostar": [], "Edision": [], "Elanvision": [], "Elap": [], "Emme Esse": [], "Emos": [], "Emtec": [], "E-Tek": [], "Eurielt/Dist": [], "Europhon": [], "Europsat": [], "Evology": [], "Evolve": [], "Eycos": [], "F.P.E.": [], "FetchTV": [], "FMD": [], "Fonestar": [], "Formenti": [], "Formuler": [], "Fortecstar": [], "Fracarro": [], "Fransat": [], "Freesat": [], "FTE": [], "Fuba": [], "Fuji Magnetics": [], "Fuji Onkyo": [], "Galaxis": [], "Gibertini": [], "GIGA BLUE": [], "GIGA TV": [], "GLOBO": [], "GLOBSAT": [], "Golden Interstar": [], "Golden Media": [], "Goobay": [], "Gosat": [], "Green Technology": [], "Hauppauge": [], "Hb": [], "HD LINE": [], "Hiremco": [], "Hirschmann": [], "Hiteker": [], "Homecast": [], "Humax": [], "I-Can": [], "Iisonic": [], "Ikusi": [], "Imex": [], "INOUTTV": [], "Intervision": [], "Intex": [], "Intuix": [], "Inverto": [], "Invion": [], "Iotronic": [], "iPlayer": [], "Iris": [], "IRON5": [], "Jok Electro": [], "Kaon": [], "Kathrein": [], "Kft": [], "Kooltek": [], "Kyostar": [], "Leader": [], "Lemon": [], "Lenson": [], "Lenuss": [], "Leyco": [], "Life View": [], "Live": [], "Lorenzen": [], "Lumax": [], "MAG": [], "Manata": [], "Maximum": [], "Mecatronica": [], "Media Price": [], "Mediasat": [], "Mediasystem": [], "Megasat": [], "Meliconi": [], "Memorysat": [], "Memup": [], "Meosat": [], "Micro": [], "MICRO ELECTRON": [], "Mirasat": [], "Moussier": [], "MTCC": [], "Multimo": [], "MVision": [], "Mysat": [], "Necvox": [], "Nedis": [], "NELI": [], "Neotion": [], "Neovia": [], "Neta": [], "Netgear": [], "Netgem": [], "Neuhaus": [], "New Line": [], "New Sat": [], "Nextwave": [], "Ninetech": [], "Noda": [], "Nokia": [], "Notonlytv": [], "Npg Tech": [], "Omenex": [], "Ondial": [], "One For All": [], "Optex": [], "Opticum": [], "OPTIMUSS": [], "Orton": [], "Pace": [], "Patriot": [], "Phonotrend": [], "Pixx": [], "Pkd": [], "Pmb": [], "Protek": [], "Pyxis": [], "Qmedia": [], "QVIART": [], "Radix": [], "Rainbow": [], "Reycom": [], "Rollmaster": [], "SAB": [], "Sat Man": [], "SATIX": [], "Seeltech": [], "Selfsat": [], "Septimo": [], "Servimat": [], "Set one": [], "Shoi": [], "Skyplus": [], "Skyworth": [], "Slingmedia": [], "Smart Line": [], "SOGNO": [], "Starcom": [], "Starland": [], "Storm": [], "SVS": [], "Systec": [], "Tahnon": [], "TCL": [], "TDT BOSTON": [], "Technomate": [], "Technosonic": [], "TechnoTrend": [], "Tecsat": [], "Tekcomm": [], "Teleciel": [], "Teleco": [], "Telenet": [], "Telesystem": [], "Televes": [], "Telit": [], "Telsky": [], "Tempo": [], "Thomsom": [], "Titan": [], "Tonna": [], "Topachat": [], "Topfield": [], "Tracer": [], "Trekstor": [], "Triax": [], "Tvnum": [], "Tvonics": [], "TV-Star": [], "Twinner": [], "Univers": [], "Univision": [], "VALUELINE": [], "Vantage": [], "Vaova": [], "Videoweb": [], "VIEW 21": [], "Visionic": [], "Visiosat": [], "Volcasat": [], "Vu+": [], "We Digital": [], "Winstec": [], "Wisi": [], "Wiwa": [], "Wizz": [], "WWIO": [], "X Trend": [], "X-Com": [], "XEOFIX": [], "XTREND": [], "ZAAP": [], "Zehnder": [], "Zircon": []},
      "c32535": {"2XL": [], "3D SOUND LABS": [], "3M": [], "4u": [], "A4 Tech": [], "Abyss": [], "Acme": [], "Acomax": [], "ACOUSTICSHEEP": [], "Actto": [], "ADL": [], "ADN": [], "Advance": [], "AEDLE": [], "AERIAL7": [], "AFTERSHOKZ": [], "Agef": [], "Aiaiai": [], "Aircoustic": [], "AirDrives": [], "Akashi": [], "AKG": [], "Alecto": [], "Alesis": [], "Allen & Heath": [], "ALPHA AUDIO": [], "Alpine": [], "Altai": [], "Aluratek": [], "Amarina": [], "American Audio": [], "AMPLICOMMS": [], "ANCUS": [], "Ansonic": [], "Antec": [], "Approx": [], "Aquapac": [], "Arctic Cooling": [], "Arkon": [], "Artwizz": [], "AS": [], "ASTELL & KERN": [], "Atari": [], "Atomic": [], "Atomic Floyd": [], "ATTITUDE ONE": [], "AUDEZE": [], "Audio Chi": [], "Audio Phony": [], "AUDIOFLY": [], "Audioquest": [], "Audio-Technica": [], "Awei": [], "B & W": [], "B&O PLAY": [], "Bandridge": [], "Bazoo": [], "BEATS": [], "BEATS BY DR.DRE-FAKE": [], "Beewi": [], "Behringer": [], "Belkin": [], "Bench": [], "beyerdynamic": [], "BIOWORLD": [], "BLACK MARKET": [], "BLOC&ROC": [], "BLUE": [], "Blue": [], "Blue Micro": [], "Bone": [], "Bookeen": [], "BOOMPHONES": [], "Boss": [], "BRAINWAVZ": [], "Breo Sport": [], "BRITISH AUDIO": [], "Brookstone": [], "BROWNIZ": [], "BST": [], "BUDDYPHONES": [], "BYZ": [], "CAMPFIRE AUDIO": [], "Campus": [], "Canyon": [], "CARDAS": [], "Case Logic": [], "Cellular Line": [], "Celsus": [], "Cepewa": [], "CHICA VAMPIRO": [], "Chord & Major": [], "Cirkuit Planet": [], "Ckp Live": [], "Clarion": [], "Clementoni": [], "Cliptec": [], "CO:CAINE": [], "Code": [], "Codiac": [], "Colors": [], "Coloud": [], "Connect": [], "Connectland": [], "Cool Device": [], "Coolbox": [], "CordCruncher": [], "Cortex": [], "Cowon": [], "Cresyn": [], "Cyber": [], "CYBERNETIC": [], "Cyberwave": [], "CYW": [], "Dacomex": [], "Dalap": [], "DC Comics": [], "DCI": [], "Dea": [], "DEA FACTORY": [], "Defender": [], "degrees": [], "Delta": [], "Dexim": [], "DGM": [], "DIESEL MONSTER": [], "Digifi": [], "Digital electronique": [], "Digitus": [], "DITMO": [], "DJ Tech": [], "Dolce Vita": [], "Dreams": [], "Dunu": [], "e5": [], "Earcandi": [], "EARIN": [], "Earsonics": [], "EBTEK": [], "Ecko": [], "Ed Hardy": [], "EDC": [], "Elecom": [], "Elro": [], "Elveco": [], "Elypse": [], "Elyxr": [], "Eminent": [], "Eneride": [], "Enermax": [], "ENIGMACOUSTICS": [], "ENZATEC": [], "Erard": [], "Eskuche": [], "ESTRELLA": [], "Etymotic": [], "Eurosound": [], "ewent": [], "EXEZE": [], "Expelec": [], "Explay": [], "Exspect": [], "Extreme": [], "FANNY WANG HEADPHONE": [], "Fantec": [], "Fatman": [], "FBI": [], "Fender": [], "FERRARI LOGIC3": [], "FIDUE": [], "Fiio": [], "FINAL AUDIO DESIGN": [], "Fischer": [], "Flair": [], "FLAVR": [], "FLIPS AUDIO": [], "Fnac": [], "Focal": [], "Fostex": [], "Fujikon": [], "Fujitsu": [], "Furutech": [], "G&B": [], "G&Bl": [], "GADGET SHOP": [], "GameOn": [], "G-Cube": [], "GEEKO": [], "Geemarc": [], "Gembird": [], "Generic": [], "German Maestro": [], "GIFTING": [], "Gigabyte": [], "GIZZYS": [], "GKIP": [], "Glam Rox": [], "gogear": [], "Golden Tech": [], "Goldring": [], "Goodis": [], "Gorsun": [], "Gourmandise": [], "Grado": [], "Grape": [], "Graphics": [], "GREEN E": [], "Groove": [], "H2O Audio": [], "HALO": [], "Hamlet": [], "Hapena": [], "Harman-Kardon": [], "Hartig+Helling": [], "Havit": [], "Headmusic": [], "Headset": [], "Hedkandi": [], "Helios": [], "Hella": [], "HESTEC": [], "Hexakit Skin Pack": [], "HIFIMAN": [], "Hi-Fun": [], "HINIC": [], "HIP STREET": [], "Hobby": [], "Hori": [], "House of Marley": [], "Hualipu": [], "Huawei": [], "HUMANTECHNIK": [], "IBASSO": [], "I-Beat": [], "Ibox": [], "Icidu": [], "Icon": [], "Iconnex": [], "Ifeelu": [], "Ifrogz": [], "Igo": [], "IHIP": [], "I-Mego": [], "IMG Stage Line": [], "IMPERII": [], "In Phase": [], "IN2": [], "inCarBite": [], "Incipio": [], "Innovate": [], "Intec": [], "In-Tune": [], "Irhythms": [], "iSkin": [], "Isound": [], "ISY": [], "ITC": [], "I-Tec": [], "ITek": [], "IWORLD": [], "J&Y": [], "J. E. Schum": [], "Jabra": [], "Jam": [], "Jaybird": [], "Jays": [], "jazwares": [], "Jb System": [], "JES Collection": [], "Jess": [], "JH AUDIO": [], "JIAXU": [], "Jivo": [], "Jlab": [], "JOK": [], "Joystyle": [], "Joytech": [], "Joytronic": [], "JUST DANCE": [], "Jwin": [], "KAM": [], "Kanon": [], "Karman": [], "KEF": [], "KENNERTON": [], "KENU": [], "KEYOUEST": [], "KEYSIU": [], "KIDDESIGNS": [], "KIDZ GEAR": [], "KIDZSAFE": [], "Kikkerland": [], "Kinyo": [], "Klipsch": [], "KLTRADE": [], "Kng": [], "Kool Sound": [], "Koopman": [], "Koss": [], "Kove": [], "Kraun": [], "KRK": [], "Kukuxumusu": [], "KURIO": [], "LASMEX": [], "LAVOLTA": [], "Lazerbuilt": [], "LDLC": [], "LEAPFROG": [], "Lenovo": [], "Lifetime": [], "Lindy": [], "Little Marcel": [], "Little Star Creations": [], "Logicom": [], "Loooqs": [], "LOSC": [], "LQP": [], "Lygo International": [], "Mac Mah": [], "Madrics": [], "Mad-x": [], "Magisound": [], "Magnat": [], "Major": [], "Maloperro": [], "Marantz": [], "MarBlue": [], "MARSHALL": [], "Marvel": [], "Master": [], "MASTER&DYNAMIC": [], "M-Audio": [], "MAXAMPERE": [], "Maxxtro": [], "Mcad": [], "MCL Samar": [], "MDC": [], "Me To You": [], "Media Express": [], "MEELECTRONICS": [], "MEENEE": [], "MERKURY INNOVATIONS": [], "MEZE": [], "MG Itex": [], "Mi": [], "Microsoft": [], "Microspot": [], "MIDBASS": [], "Mielco": [], "Ministry of Sound": [], "Mitchell & Johnson": [], "Mitone": [], "Mitsubishi": [], "Mix Style": [], "Mlb": [], "Mobilecast": [], "Mobilegear": [], "Modecom": [], "MOKI": [], "Monacor": [], "MONOPRICE": [], "Moshi": [], "MOTÖRHEAD PHÖNES": [], "Mr Men": [], "Mr. Handsfree": [], "MRSPEAKERS": [], "Mtv": [], "MTX Audio": [], "Multilaser": [], "Musical-Fidelity": [], "Musicman": [], "Muvit": [], "MY DOODLES": [], "My Little Pony": [], "My Way": [], "MYKRONOZ": [], "NAD": [], "Natec": [], "Nathan Multimedia": [], "Ndeo": [], "NEKLAN": [], "Neonumeric": [], "Network": [], "Newtech": [], "Nextbase": [], "Nike": [], "Nintendo": [], "Nixon": [], "No.1": [], "Noble": [], "NOONTEC": [], "Novistar": [], "NU FORCE": [], "Numark": [], "OCULUS": [], "OID Magic": [], "ONANOFF": [], "ONE DIRECTION": [], "ONE SOUND": [], "OnePlus": [], "Onkyo": [], "Onyx": [], "Oppo": [], "Opus": [], "ORA": [], "Osaki": [], "OTL": [], "Out of the blue": [], "OUTDOOR TECHNOL": [], "Over Board": [], "Pataco": [], "PAW PATROL": [], "Peltor": [], "Peppa Pig": [], "Phiaton": [], "Philips O'Neil": [], "Philips Swarovski": [], "PHONAK": [], "Phonia": [], "Phonix": [], "Phonocar": [], "PHONON": [], "Piranha": [], "Pirelli": [], "Playfect": [], "Pleomax": [], "Pole Star": [], "Polk Audio": [], "Porsche Design": [], "Port": [], "Power Star": [], "Powerdynamic": [], "Premium": [], "PreSonus": [], "Printlight": [], "Pro.2": [], "Prodipe": [], "Pro-Ject": [], "Proporta": [], "Prostima": [], "PSB": [], "Puma": [], "Puro": [], "Qonix": [], "QTX": [], "QUARKIE": [], "Qube": [], "QUDO": [], "Quicksilver": [], "QUIETON": [], "Rabbit": [], "Radiopaq": [], "Raidsonic": [], "Rapoo": [], "Raptor Gaming": [], "Raxconn": [], "Razer": [], "READY2MUSIC": [], "REC8": [], "RECCO": [], "RED4POWER": [], "Reekin": [], "Reloop": [], "RETRAK": [], "RHA": [], "Ritmix": [], "R-MUSIC": [], "ROCK JAW": [], "Rocking Residence": [], "Roland": [], "Rony": [], "Ross": [], "RUGBY DIVISION": [], "RUNPHONES": [], "RUNTASTIC": [], "RYGHT": [], "Sadim": [], "Saitek": [], "Saiyo": [], "Samson": [], "Sandberg": [], "Scholastic": [], "Scosche": [], "SECTION8": [], "Sennheiser": [], "SENNHEISER-FAKE": [], "Setty": [], "SEVA IMPORT": [], "SHARK BISCUIT": [], "Shike": [], "Shure": [], "SKINNYSOUND": [], "Skpad": [], "Skullcandy": [], "SLEEK AUDIO": [], "SLEEPPHONES": [], "SMART SYSTEM": [], "SMS": [], "SMS AUDIO": [], "Snakebyte": [], "SOGT": [], "SOL REPUBLIC": [], "Sonic": [], "Sonorous": [], "Sonus Faber": [], "Soul": [], "Soundlab": [], "SoundMagic": [], "Soyntec": [], "Speed Link": [], "Spyker": [], "Stagg": [], "Stanton": [], "Stax": [], "Steel Series": [], "Studioline": [], "SUOJUN": [], "SUPER BASS": [], "Super star": [], "Superlux": [], "Sven": [], "Swarovski": [], "Sweet Years": [], "Sylbert": [], "TabZoo": [], "TAIDEN": [], "takeMS": [], "Takstar": [], "Targus": [], "Tascam": [], "TEC PLUS": [], "Teccus": [], "Technics": [], "Temium": [], "Templar": [], "The T.Bone": [], "Thesys": [], "THINKSOUND": [], "Thrustmaster": [], "Time4Tech": [], "TINTEO": [], "Titanum": [], "TNB": [], "TONINO": [], "TOYS R US": [], "Transcend": [], "Transmedia": [], "Travel Blue": [], "Trendz": [], "Tribe": [], "TRINITY": [], "TT ESPORT": [], "Tubesurround": [], "Tunewear": [], "Turbo X": [], "Turbosound": [], "TV Ears": [], "Twitfish": [], "TX Think Xtra": [], "Ubisoft": [], "Ultimate Ears": [], "Ultrasone": [], "UNEED": [], "Uniformatic": [], "Uniross": [], "Unitone": [], "Universal Music": [], "URBAN REVOLT": [], "Urban Tech": [], "Urbanears": [], "Urbanz": [], "Uunique": [], "V7 Videoseven": [], "Variance": [], "VEEBEES": [], "Veho": [], "Velleman": [], "Velodyne": [], "Venom": [], "Vestax": [], "Vic Firth": [], "Vivanco": [], "V-Moda": [], "Vox": [], "VST": [], "WAATECK": [], "WATS": [], "Wavemaster": [], "WESC": [], "Westone": [], "Wintech": [], "Wize & Ope": [], "Wraps": [], "X-1": [], "Xqisit": [], "XSORIES": [], "Xtreamer": [], "XX.Y": [], "Yougs": [], "Yours": [], "YURBUDS": [], "YZSY": [], "Zagg": [], "Zalman": [], "Zenec": [], "ZEST": [], "ZIPBUDS": [], "ZIPERD": [], "Zip-Linq": [], "Zumreed": []},
      "c32539": {"Abus": [], "ACME Made": [], "Actioncam": [], "ACTIONPRO": [], "ACTIVEON": [], "AEE": [], "airwheel": [], "Amyola": [], "ANDOER": [], "APOTOP": [], "Beaulieu": [], "BILLOW": [], "Blackmagic Design": [], "Bosch-Bauer": [], "Braun Phototechnik": [], "Braun-Nuernberg": [], "Bullet": [], "Camlink": [], "CAMONE": [], "CHILLI TECHNOLOGY": [], "Clickles": [], "Contour": [], "C-Tech": [], "Delium": [], "Delkin Devices": [], "Disgo": [], "DJI": [], "Drift Innovation": [], "ELE": [], "E-TIGER": [], "EXCELVAN": [], "Eyenimal": [], "EZVIZ": [], "Feiyu": [], "Fisher": [], "Flip Video": [], "FREE RIDE": [], "FREERIDERS": [], "Garmin": [], "Geco": [], "Geonaute": [], "Giroptic": [], "GOBANDIT": [], "GOXTREME": [], "Guncam": [], "Haldex": [], "Halterrego": [], "Hanseatic": [], "HD": [], "HIREC": [], "HOMIDO": [], "HTC": [], "Hy Technology": [], "Insta360": [], "Isaw": [], "JJA": [], "Jobo": [], "Kaiser Baas": [], "KEQU": [], "Kitvision": [], "Kmax": [], "Konix": [], "Lava": [], "Liquid image": [], "Little Acorn": [], "L-LINK": [], "Loewe": [], "MCA TECHNOLOGY": [], "Mediacom": [], "Metz": [], "Mevo": [], "MIO": [], "Mobius": [], "MOFILY": [], "MONSTER DIGITAL": [], "MYWI": [], "National Geographic Deutschland": [], "NAVICOM": [], "Nexxt Idea": [], "Numaxes": [], "OEM": [], "OMEGA": [], "opticam": [], "Ordro": [], "PANONO": [], "PANOX": [], "PQI": [], "Protax": [], "Qantik": [], "QimmiQ": [], "QUMOX": [], "R'BIRD": [], "REDKEYS": [], "REMOVU": [], "rePLAY XD": [], "RIDEVIZION": [], "ROADHAWK": [], "RunCam": [], "Ryval": [], "SJCAM": [], "Somikon": [], "Spypen": [], "SUNNYCAM": [], "Tamron": [], "Teamsport": [], "TECTECTEC!": [], "TomTom": [], "UNIQAM": [], "Universum": [], "VOG": [], "VUZE": [], "WATER WO": [], "WEMOOVE": [], "Wolder": [], "XBASE": [], "Xiaomimi": [], "X'TREM": [], "XTREME-CAMERA": [], "X-ZERO": [], "YI": [], "YUNEEC": [], "YUTECH": [], "YUWATCH": [], "Zaptub": [], "Z-CAM": [], "Zoom": []},
      "c32547": {"Adafruit": [], "Adentec": [], "ADI": [], "Advantech": [], "AG Neovo": [], "AGM": [], "Alapage": [], "Albatross": [], "Albiral": [], "Alienware": [], "AMW": [], "Amx": [], "AOC": [], "Aputure": [], "Arduino": [], "ARTHUR HOLM": [], "AST": [], "Atec": [], "ATOMOS": [], "AURES": [], "AVidAV": [], "Avidsen": [], "Avocent": [], "Avtek": [], "AXIOMTEK": [], "Barco": [], "Bdmc": [], "BEETRONICS": [], "Belinea": [], "Blueh": [], "Bluem": [], "Bowers": [], "Brimax": [], "Bull": [], "Byron": [], "C.Edison": [], "Captiva": [], "Cdiscount": [], "Chimei": [], "Chinavasion": [], "Cibox": [], "Cisco": [], "Claxan": [], "Cmv": [], "Colortac": [], "Comelit": [], "Commodore": [], "Compaq": [], "Cornea": [], "Cornerstone": [], "Crestron": [], "CTOUCH": [], "CTX": [], "Cx": [], "Dabsvalue": [], "DEC": [], "Deltaco": [], "Di-Fusion": [], "Digital": [], "Direction": [], "Dynascan": [], "Edge10": [], "Eizo": [], "Elettrodata": [], "Elo Touchsystems": [], "Elonex": [], "Elyxio": [], "Emachines": [], "Eneo": [], "Envision": [], "Escom": [], "Esys": [], "ETC": [], "EURO CLS": [], "Eurocase": [], "Extron": [], "E-Yama": [], "Eyestoeyes": [], "Faytech": [], "FEC": [], "Flytech": [], "Formac": [], "Fujicom": [], "Futura": [], "GAEMS": [], "Gateway": [], "GECHIC": [], "Genee World": [], "General Touch": [], "Generico": [], "Generique": [], "GEO": [], "Gericom": [], "Glancetron": [], "GNR": [], "GNX": [], "GVision": [], "Hanns.G": [], "Hannstar": [], "Hansol": [], "Hantarex": [], "Hanton": [], "Hanwha Japan": [], "Harimax": [], "Highscreen": [], "HIKVISION": [], "Hitech": [], "Hivision": [], "HKC": [], "Hpc": [], "HUION": [], "Hymer": [], "Hyundai It": [], "iBoardTouch": [], "IEI": [], "IF": [], "I-Inc": [], "Iiyama": [], "IKAN": [], "Imax": [], "Infocus": [], "Innes": [], "Innopaq": [], "Innovative": [], "Iolair": [], "IPO TECHNOLOGIE": [], "Ipure": [], "Iqon": [], "Irts Display": [], "Jdr Computer Products": [], "Jean": [], "Joy-It": [], "KDS": [], "Lacie": [], "Lancom": [], "Legamaster": [], "Likom": [], "Lilliput": [], "Liteon": [], "Liteview": [], "LUMON": [], "Macom": [], "Maguay": [], "Marshall": [], "Maxdata": [], "Mermaid": [], "Microtouch": [], "Mimo": [], "MIP": [], "Mirai": [], "Miro": [], "Misco": [], "Mitac": [], "Modulux": [], "Monxx": [], "Monyka": [], "Msi": [], "Multi Q": [], "Nagasaki": [], "Nano": [], "NCR": [], "Nech": [], "NEWLINE": [], "Nfren": [], "Nits": [], "Novita": [], "Nvision": [], "NVOX": [], "Ocegraphics": [], "Octigen": [], "Olevia": [], "Olidata": [], "Origen": [], "ORION TECHNOLOGY": [], "Otek": [], "Panoview": [], "Partenio": [], "Partner Tech": [], "Pc Note": [], "Peacock": [], "PEERLESS": [], "Pixmania": [], "Planar": [], "Polycom": [], "Polyview": [], "Posiflex": [], "POSLAB": [], "Princeton": [], "Process Tech": [], "PRO-FACE": [], "Promethean": [], "Proview": [], "Quato": [], "Racer": [], "Radius": [], "Rapcom": [], "RASPBERRY": [], "Rivertech": [], "Ryoku": [], "Sahara": [], "Samko": [], "Samtron": [], "Sdc": [], "Seezen": [], "Sensy": [], "SEYPOS": [], "Shuttle": [], "Sinocan": [], "Sliding": [], "Smart Media": [], "SMARTWARES": [], "Smile": [], "SolTec": [], "SPECKTRON": [], "Starplus": [], "SUN": [], "Sunbook": [], "Suyama": [], "Swedx": [], "Switel": [], "Synco": [], "Syscom": [], "Tactyl Services": [], "Tandberg": [], "Tatung": [], "Taxan": [], "Tecna": [], "Tekneo": [], "Terra": [], "Textorm": [], "Time": [], "TOGUARD": [], "Top Elite": [], "Top Vision": [], "Topcon": [], "Topview": [], "Totoku": [], "TPV": [], "Transtec": [], "Twinhead": [], "Unika": [], "Value": [], "Vibrant": [], "Victor": [], "View&Sonic": [], "Viewell": [], "Viewsonic": [], "VITY": [], "Wacom": [], "Walimex": [], "Wewa": [], "Wincor Nixdorf": [], "Winmate": [], "Winsonic": [], "Wisetech": [], "Wyse": [], "X2gen": [], "Xiod": [], "Xpola": [], "Yashi": [], "Yuraku": [], "Yusmart": [], "Zenith": []},
      "c32548": {"A Video": [], "Acoustic Solutions": [], "Admea": [], "Advance Acoustic": [], "Aitro": [], "Alco": [], "Alize": [], "Altrasonic": [], "Amuser": [], "Apex": [], "Arcam": [], "Artman": [], "ASTD": [], "Astron": [], "Astry": [], "Atacom": [], "Atoll Electronique": [], "A-Trend": [], "Audiobahn": [], "Bazzix": [], "BBK": [], "Becker": [], "Bellagio": [], "Bloom": [], "Blue:Sens": [], "Boghe": [], "Bom": [], "BRILIANT": [], "Brothers": [], "Casablanca": [], "Cdmc": [], "Cello": [], "Changjia": [], "Cilo": [], "Cinetec": [], "CJ": [], "Classé Audio": [], "Contel": [], "Curtis": [], "Cybercom": [], "Daytek": [], "Daytron": [], "Delphi Grundig": [], "Desay": [], "Difrnce": [], "Digix": [], "Digixmedia": [], "DK Digital": [], "DMC": [], "Dmtech": [], "Doriland": [], "E:Max": [], "E-Dem": [], "Electrocompaniet": [], "ERA": [], "EVD": [], "Fifty": [], "FIT": [], "Fredikson": [], "Funai": [], "Giec": [], "Golden Rich": [], "Gowell": [], "GVG": [], "Harmony": [], "Haymedia": [], "HIGH-TECH PLACE": [], "Hillteck": [], "Himage": [], "Home Electronic": [], "Home Power": [], "Homita": [], "Inovix": [], "Kaford": [], "Kazuki": [], "Keyplug": [], "King Vision": [], "Kiss": [], "KLH": [], "Kxd": [], "Laboratory": [], "Lexia": [], "Lifetec": [], "Limit": [], "Linn": [], "Linuo": [], "Liros": [], "Loomax": [], "Luxman": [], "Maitec": [], "Mc Intosh": [], "Meridian": [], "Messo": [], "Micromega": [], "Minton": [], "Mizuda": [], "MP ELECTRONICS": [], "Myryad": [], "N.T.P.": [], "Neuston": [], "Newtone": [], "Ninco": [], "NRJ": [], "Nu": [], "Olitec": [], "OLSENMARK": [], "Oritron": [], "P&J": [], "Palladine": [], "Panda": [], "Phocus": [], "Pilot Nic": [], "Primare": [], "Prinz": [], "Pro²": [], "Projectiondesign": [], "Promaster": [], "Proton": [], "Quali-TV": [], "Quartek": [], "REX": [], "Rotel": [], "Rowsonic": [], "SB": [], "Scanmagic": [], "Seal": [], "Seelver": [], "Sevic": [], "Shanghai": [], "Sherwood": [], "Shinco": [], "Shindo": [], "Siemssen": [], "Siltex": [], "Simbio": [], "Sinivision": [], "SMC.Stallmann": [], "Soniko": [], "Speed Sound": [], "Starclusters": [], "Starlite": [], "Stein": [], "Strato": [], "Sumvision": [], "Sunwood": [], "Superior": [], "SVC": [], "Takada": [], "Techlux": [], "Techma": [], "Technika": [], "Techtron": [], "Tecnimagen": [], "Teknika": [], "Tendances": [], "Texon": [], "TG": [], "Thule": [], "Transconti": [], "Trans-Continents": [], "Transgear": [], "Trinity": [], "TSM": [], "Tyme": [], "Universal Uos": [], "Upteck": [], "Vatech": [], "VEREZANO": [], "Viewfun": [], "Voxon": [], "Voyager": [], "Vtrek": [], "Wilson": [], "Xeos": [], "Xonum": [], "Yamakawa": [], "YARVIK": [], "Zanon": [], "Zicplay": []},
      "c32553": {"Aigger": [], "ART&CUISINE": [], "Avdi": [], "Azura": [], "BOP": [], "Botti": [], "Carlton": [], "Carrera": [], "cecotec": [], "Changli": [], "Clean Maxx": [], "Concept": [], "Cora": [], "Di Quattro": [], "Diana": [], "Dicaff": [], "Dieselit": [], "Duke": [], "Ecova": [], "Eltronic": [], "Esse 85": [], "Eternity": [], "Euroflex": [], "Ferrari": [], "First": [], "Fiseldem": [], "Fogacci": [], "Fortex": [], "Go Travel": [], "Goodway": [], "Hailo": [], "Hinari": [], "Hoffmanns": [], "Hugin": [], "Hydro": [], "Imetec": [], "INTERIOR": [], "Jagua": [], "JRD": [], "Jrr Electronique": [], "Kaercher": [], "KEIM HOUSE": [], "Kiti Pro": [], "Kiwi": [], "KLINDO": [], "KOENIC": [], "Laurastar": [], "Leifheit": [], "L'El-It": [], "Libellule": [], "Maitop": [], "Metalnova": [], "Micromark": [], "MONEUAL": [], "Nordland": [], "Pfaff": [], "Practica": [], "Prodis": [], "Prym": [], "Remington": [], "RGK": [], "Rhonalvap": [], "Robby": [], "SANEO": [], "Saturn": [], "Saxel": [], "SHG": [], "Shinelco": [], "Silva": [], "Silverstone": [], "SMART STEAM": [], "Speedline": [], "STEAMONE": [], "Sunbeam": [], "TECHNO": [], "TEKNOSTEAM": [], "Travel Smart": [], "Trikado": [], "Vapex": [], "Vapoline": [], "Vaporella": [], "Vapornet": [], "Vitek": [], "Xelance": [], "XSQUO": [], "Zephyr": []},
      "c32557": {"A.Marque": [], "Ankarsrum": [], "Aura": [], "Bamix": [], "Beaba": [], "Bellini": [], "BEST OF TV": [], "bianco di puro": [], "Bimar": [], "Blendicook": [], "Blendtec": [], "Brabantia": [], "Brano": [], "Buffalo": [], "CEEA ROBOT MAXI CHEF": [], "Chef": [], "Climaselect": [], "Comelec": [], "Conti": [], "Cooks Professional": [], "CUCCINA": [], "Cucina": [], "Cuisichef": [], "Cyril Lignac": [], "Dalkyo": [], "Detoximix": [], "DOMOTECH": [], "Ds": [], "DURAND DUPONT": [], "Dynamic": [], "E.ZICHEF": [], "ECO-DE": [], "ELEKTRA LINE": [], "Esge": [], "Essentials": [], "ETA": [], "Euro Wave": [], "Eurowave": [], "Feller": [], "Figuine": [], "Flama": [], "FLAVORFULL": [], "Foodmatic": [], "Franklin": [], "Fritel": [], "G21": [], "Gio'Style": [], "GOURMET GADGETRY": [], "GOURMET TOOLS": [], "GSC": [], "Guangdong": [], "Hagen": [], "Happy Cook": [], "Hawkins": [], "HELD": [], "Hendi": [], "HERENTHAL": [], "Herzberg": [], "Homekraft": [], "Homemaker": [], "Ideas": [], "Jata electro": [], "Jtc": [], "Jupiter": [], "Kai": [], "Kisag": [], "Kitchen Cook": [], "KITCHEN FRIDAY": [], "KITCHEN MANAGER": [], "KITCHEN-GRAND-C": [], "KUVINGS": [], "Laica": [], "Lenoir": [], "Lifestyle": [], "LITTLE BALANCE": [], "Look For": [], "LOUIS TELLIER": [], "Luxe": [], "Magic Bullet": [], "Magic Maxx": [], "MAN": [], "MARC VEYRAT": [], "Martin Berasategui": [], "MAYBAUM": [], "Melissa": [], "Mini Chef": [], "Miogo": [], "Mix-N-Mix": [], "Montiss": [], "Mr.Magic": [], "Mywave": [], "NEWCHEF": [], "Nikai": [], "Ninja": [], "Noon": [], "NUTRIBULLET": [], "Ohmex": [], "OmniBlend": [], "ONE TOUCH BULLE": [], "Optima": [], "Orava": [], "Oxo": [], "PANGEA": [], "Passat": [], "Philips AVENT": [], "PRADEL PREMIUM": [], "Prolectrix": [], "Red Line": [], "Redmond": [], "Relaxdays": [], "Robot Coupe": [], "Ronic": [], "ROSLE": [], "Salter": [], "Samix": [], "Saphir": [], "Scaroni": [], "SCHEFFLER": [], "Schenzhen": [], "SCHMIT": [], "SECRET DE GOURM": [], "SelectLine": [], "SHAKE N' GO": [], "Shivn Feng": [], "SINOTECH": [], "SMOOTHIE XPRESS": [], "Sonashi": [], "Superchef": [], "Supercook": [], "SWEETALICE": [], "Tarrington House": [], "Team Kalorik": [], "Terraillon": [], "T-Fal": [], "Trebs": [], "TRIBEST": [], "Turbotronic": [], "TV UNSER ORIGIN": [], "Ultramaxx": [], "Venteo": [], "VitaMix": [], "Vivre Mieux": [], "Vortex": [], "Waring": [], "YAMMI": [], "YUECHING": [], "ZEN & PUR": [], "Zyliss": []},
      "c32561": {"A & C": [], "Agait": [], "Agama": [], "Alfatec": [], "Aquavac": [], "Arle": [], "ASPIROMATIC": [], "ASPIRON": [], "Astel": [], "Bavaria": [], "BE PRO": [], "Beldray": [], "Birum": [], "Bissell": [], "Bliss": [], "Blitz": [], "BLUE BELL APRC": [], "bObsweep": [], "Bork": [], "Bricotech": [], "Britania": [], "Broszio": [], "Build Worker": [], "Builder": [], "Car +": [], "CENOCCO": [], "CEVIK": [], "Cevylor": [], "Clean Star": [], "Clean Up": [], "Cleanfix": [], "CLEANING": [], "Cleanmate": [], "Contact": [], "Corner": [], "Crazy": [], "Cyclonia": [], "Davo": [], "Daya": [], "DEEBOT": [], "Defort": [], "Delfin": [], "Delta Jet": [], "Deltaspire": [], "Dexter Power": [], "Dilem": [], "Dimin": [], "DIRT BULLET": [], "Dirt Devil": [], "Dirt Hunter": [], "Dolce Casa": [], "E.Ziclean": [], "Earlex": [], "Ecodrop": [], "Ecovacs": [], "Eder": [], "Edison": [], "Eio": [], "El Fuego": [], "Electro-Line": [], "Electromix": [], "Elekta": [], "Elektro Maschinen": [], "Elem/Technik": [], "Elin": [], "Emer": [], "Eufab": [], "Eurasia": [], "EUROBOTS": [], "Eurom": [], "EUROMENAGE": [], "Ewbank": [], "EWT": [], "Excelsa": [], "Expressline": [], "FAM": [], "Far Tools": [], "Favel": [], "Feider": [], "Fein": [], "Feroe": [], "Fersen": [], "Festool": [], "Fiac": [], "FIELDMANN": [], "Finetech": [], "Flex": [], "Floor Zoom": [], "Gardena": [], "Germatic": [], "Ghibli": [], "Gisowatt": [], "Glen Dimplex": [], "Goblin": [], "Goodyear": [], "Greenworks": [], "Guzzanti": [], "Haeger": [], "HETTY": [], "Hilti": [], "Holland": [], "Home Angel": [], "HOME CLUB": [], "Home Talent": [], "Homefriend": [], "IDE Line": [], "IDEAL HOME": [], "Impex": [], "Incasa": [], "Indomo": [], "Intertronic": [], "Irobot": [], "Ironside": [], "Ismet": [], "Italvas": [], "JE CHERCHE UNE": [], "K&": [], "Kawasaki": [], "KENNEX/TB": [], "KENSTON": [], "Kinzo": [], "KOMOBOT": [], "KOTEL": [], "Kraft": [], "Kress": [], "L'Aspirateur": [], "Lavor": [], "Lavorwash": [], "Leman": [], "Leroy Merlin": [], "Lervia": [], "Linea Casa": [], "LINEA TIELLE": [], "Liv": [], "Mac Allister": [], "MAGIC UV": [], "MAMIROBOT": [], "Mannesmann": [], "Mastrad": [], "Matrix": [], "Mauk": [], "MAX": [], "Maxipower": [], "Mazda": [], "Mc Kenzie": [], "MD": [], "Mda": [], "Meister": [], "Mejix": [], "Melchioni": [], "Michelin": [], "Mr Buddy": [], "Muter": [], "Neato Robotics": [], "Necchi": [], "NEWTECK": [], "Nilfid": [], "Nilfisk": [], "Nilfisk-Alto": [], "NODIS": [], "NOVELLY": [], "Novipro": [], "Numatic": [], "Numero 1": [], "Oase": [], "ok.": [], "OTOKIT": [], "PARIS RHONE": [], "Parkside": [], "Perel": [], "Performair": [], "Performance Power": [], "Petit": [], "Peugeot": [], "Plihal": [], "Polaris": [], "Power Plus": [], "Powervac": [], "Practyl": [], "Prixton": [], "Profi": [], "Prologic": [], "Promac": [], "PROVAC": [], "RAVLINE": [], "Raycop": [], "Redstone": [], "Rhino": [], "Ribimex": [], "Ribitech": [], "Ring": [], "Robomop": [], "Rohs": [], "Rondy": [], "Rotary": [], "RUMBOT": [], "SAUGKRAFT": [], "Sebo": [], "Shivaki": [], "Shopvac": [], "Sidamo": [], "Simec": [], "Simmons": [], "Simpa": [], "Simpex": [], "Sisal": [], "Skil": [], "Solfacil": [], "Sona": [], "Sonnenkönig": [], "Sopadis": [], "SP`D Clean": [], "Sparco": [], "Speedclean": [], "Spit": [], "Stayer": [], "Steamatic": [], "Stihl": [], "Sumex": [], "Sunny": [], "Super Clean": [], "SUPERTEK": [], "Swivel": [], "Syclone": [], "Tango": [], "Technic": [], "Tekvis": [], "Teleshop": [], "Terraclean": [], "The Boss": [], "Thoshiro": [], "TLJ": [], "Tokina": [], "TORNADO": [], "Trendy Color": [], "TSB": [], "Tudor": [], "Twister": [], "Ubbink": [], "ULYSSE": [], "Vacmaster": [], "Varo": [], "VAX": [], "Vetrella": [], "Vigor": [], "Vileda": [], "Viper": [], "Volta": [], "Vorwerk": [], "Windmere": [], "WOLPERTECH": [], "X5 VAC": [], "X6": [], "Zinatic": [], "ZYGOSHOP": []},
      "c32562": {"Arrow": [], "CITIZENS": [], "Corbero": [], "Domest": [], "Fde France": [], "Fensa": [], "Gebhardt": [], "Glem-Gas": [], "Husqvarna": [], "Jollynox": [], "Kehl": [], "LA Cornue": [], "Laclanche": [], "Lofra": [], "Luxell": [], "Mora": [], "M-Systems": [], "Mumsig": [], "NED": [], "New World": [], "Oven Plus": [], "PER": [], "Privileg": [], "Restpoint": [], "Savoir": [], "Segad": [], "Setra": [], "Siul": [], "Sogedis": [], "Sonai": [], "Technogas": [], "Triumph": [], "Universal": [], "Waltahm": [], "Westahl": [], "Zanussi-Electrolux": []},
      "c32632": {"Aaeon Technology": [], "AAT": [], "Absolut": [], "Actina": [], "ACTION": [], "ADJ": [], "Adonia": [], "ADS-Tec": [], "Aerocool": [], "Akasa": [], "A-Link": [], "ALIX": [], "Alphacom": [], "Alphamedia": [], "Alternate": [], "ALZA": [], "Amazon": [], "Amerry": [], "ANKERMANN COMPUTER": [], "Aopen": [], "APC": [], "API Computer": [], "Aquarius": [], "ARI": [], "ASRock": [], "Athena": [], "Autocont": [], "Avaya": [], "Avi Micro": [], "AVNET": [], "AWOX": [], "Axel": [], "Axis": [], "AZIROX": [], "AZULLE": [], "BACATA": [], "Banana": [], "Beagleboard": [], "BEELINK": [], "Biostar": [], "Birch": [], "BLACKLINE": [], "BlackStorm": [], "Bluechip": [], "Bogo": [], "Camtrace": [], "CAPTURE": [], "Cheap": [], "Chiligreen": [], "Chip PC": [], "Cirque": [], "CITTADINO": [], "clientron": [], "Colormetrics": [], "Comfor": [], "COMPUDEALS": [], "Compunet": [], "Compupro": [], "Cooler Master": [], "Corsair": [], "CORUS": [], "Crane": [], "Cybershop": [], "Cybertek": [], "Cyrus": [], "CZC": [], "Danew": [], "Data Graphic": [], "Datapath": [], "Decimal": [], "Depo": [], "DG-Micro": [], "Di": [], "Differo": [], "Digicom": [], "Digipos": [], "Digipro": [], "D-Link": [], "DROIDPLAYER": [], "DTK": [], "DUNE HD": [], "Dustin": [], "Dynamode": [], "EALTEC": [], "ECRIN": [], "ECS": [], "Egreat": [], "EID": [], "Ei-System": [], "Elitegroup": [], "Epa": [], "Epatec": [], "Erel": [], "Ernitec": [], "Event": [], "Evga": [], "Exone": [], "Factory": [], "Flextron": [], "Forcast": [], "Foxconn": [], "FT": [], "Game Lander": [], "gecCOM": [], "Giada": [], "Gigabox": [], "Gigasys": [], "GOALLTV": [], "Google": [], "H96": [], "Hal3000": [], "HardKernel": [], "Hardware Outlet": [], "HIMEDIA": [], "HIPER": [], "Home": [], "Honeywell": [], "HUMELAB": [], "Husk Tech": [], "Hyrican": [], "ICARICIO": [], "Igel": [], "IGGUAL": [], "Ikom": [], "Impression": [], "Infinity": [], "Inforsud": [], "Inmac": [], "Inno3d": [], "Integris": [], "Intelbras": [], "Intermec": [], "Intertech": [], "Inves": [], "IPC2U": [], "Itium": [], "Jetway": [], "Juniper Networks": [], "Kaiwin": [], "Kapcom": [], "Kelyx": [], "Kerti": [], "KIANO": [], "Komputronik": [], "KUBB": [], "L.G.L. Dev": [], "LANNER": [], "LC Power": [], "Leadtek": [], "Legend": [], "Lineane": [], "Longshine": [], "Lynx": [], "Majesty": [], "Mansoft": [], "Marcopoly": [], "MEASY": [], "Mede8er": [], "Mesh": [], "MGD": [], "MIB": [], "Micdis": [], "Micro Tech": [], "Microllenium": [], "Micromaxx": [], "Microstar": [], "Minix": [], "Morex": [], "MR. MICRO": [], "MSG": [], "Ms-Net": [], "Multimedis": [], "MXQ": [], "MYGICA": [], "nabi": [], "Nantesmicro": [], "Nausicaa": [], "NComputing": [], "NDIS": [], "Nemo": [], "NEOUSYS TECHNOL": [], "Neoware": [], "Newdata": [], "Nexcom": [], "Next": [], "NEXXT": [], "Nirva": [], "Norrod": [], "Novotec": [], "NOW TV": [], "NURVO": [], "Nutanix": [], "Nvidia": [], "Oceanet": [], "Ocem": [], "ODX": [], "Oldi": [], "One": [], "OnePc": [], "OpenHour": [], "Optimus": [], "Oracle": [], "Ordissimo": [], "Orgelec": [], "PanOcean": [], "Paradise": [], "Pc 2000": [], "PC ENGINES": [], "Pc Tek": [], "PC Wave": [], "Pc.Kube": [], "Pci": [], "Pegasus": [], "Pegatron": [], "Penta": [], "Perimetre": [], "Phoenix": [], "Planet Elektronik": [], "Platin": [], "POINDUS": [], "Point-Of-View": [], "Popcorn Hour": [], "Powernet": [], "PRAIM": [], "Premio": [], "Primux": [], "PRODVX": [], "Pyramid": [], "Q Motion": [], "QNAP": [], "Quanta": [], "Quest": [], "Rangee": [], "RASPBERRY PI": [], "Rikomagic": [], "Roku": [], "Rombus": [], "SAGA": [], "Sapphire": [], "SEDATECH": [], "Sequence": [], "Serioux": [], "Simplivity": [], "Sitten": [], "Skynet": [], "SolidRun": [], "Sonbook": [], "Spacebr": [], "Speechi": [], "Staris": [], "STORITE": [], "Supercomp": [], "Supermicro": [], "Surcouf": [], "Systea": [], "Systeam": [], "Tandy": [], "Tarox": [], "TENGO": [], "Tesenca": [], "THOR": [], "Titeck": [], "TIZZBIRD": [], "TKF": [], "Top Station": [], "Traxdata": [], "Trend": [], "Triline": [], "TRONSMART": [], "Tsunami": [], "Tulip": [], "TWC": [], "Twintech": [], "Tyan": [], "Tysso": [], "U.P.I": [], "Ubiquiti": [], "Ultimo": [], "ULTRATECH": [], "Ultron": [], "Underwood": [], "Upvel": [], "Veci": [], "VECTREX": [], "VEKOBS": [], "VENZ": [], "Vero": [], "VIA": [], "Vibox": [], "Vision": [], "vivapos": [], "Vivitek": [], "VXL": [], "Western Digital": [], "Wetek": [], "Wibtek": [], "Winblu": [], "Winner": [], "Workey": [], "XLYNE": [], "Xtratech": [], "Yatoo": [], "Zebra": [], "ZEETIM": [], "Zidoo": [], "Zoostorm": [], "Zotac": []},
      "c32643": {"1IDEA": [], "1MORE": [], "2Go": [], "4-OK": [], "4SMARTS": [], "A+": [], "Abe": [], "AC": [], "AC Unicell": [], "Accessorize": [], "Accuratus": [], "Accutone": [], "Addict": [], "ADIBLA": [], "ADVANCED ACCESSORIES": [], "AFTERGLOW": [], "Agatha R. Prada": [], "Agfeo": [], "Aiino Style": [], "AILIHEN": [], "AIR": [], "Akito": [], "AKYTA": [], "Aliph": [], "Allgon": [], "ALPHA OMEGA PLA": [], "Alpha Secom": [], "AMPLIFY": [], "Andrea": [], "Andrew": [], "ANIMA": [], "Anycom/RFI": [], "APACHIE": [], "Apcom": [], "Apple-Fake": [], "AQUAMIX": [], "Arcas": [], "Arcotec": [], "Ardt": [], "Arp Datacon": [], "ART": [], "AS-MOBILITY": [], "ASTRO GAMING": [], "Aswo": [], "AUDÉO": [], "Audionic": [], "Auerswald": [], "AUKEY": [], "AULA": [], "Auro": [], "Av Link": [], "AVANCA": [], "Avantalk": [], "AVANTREE": [], "Avizar": [], "Avo": [], "AVO+": [], "Avro": [], "Axes": [], "Axtel": [], "Azona": [], "BASEUS": [], "BASSBUDS": [], "BAT MUSIC": [], "Battrex": [], "Beeper": [], "BenQ-Siemens": [], "Benross": [], "BERSERKER GAMING": [], "Bhs": [], "Bitfenix": [], "Black Box": [], "Black Platinum": [], "Blackberry": [], "BLACKBERRY-FAKE": [], "Blaze": [], "BLOODY": [], "blu:s": [], "Blue Star": [], "Blueant": [], "Bluedio": [], "Bluenext": [], "Bluespoon": [], "Bluestar": [], "Bluetake": [], "Bluetalk": [], "Bluetooth": [], "Bluetrade": [], "Bluetrek": [], "Blueway": [], "BLUEXTEL": [], "B-Move": [], "BOAS": [], "Body Glove": [], "Boeder": [], "BOOMPODS": [], "BOOSTER": [], "Boulanger": [], "BOVON": [], "BOWER": [], "BRAGI": [], "Brigmton": [], "B-Speech": [], "Btk": [], "Cabstone": [], "CAEDEN": [], "CALIBUR11": [], "Callate la Boca": [], "Callstel": [], "Capcom": [], "Cardo": [], "CASEINK": [], "Casino Famili": [], "Cellink": [], "Cellman": [], "Celly": [], "CHICBUDS": [], "Clarity": [], "Clip&Talk": [], "Cm Storm": [], "Coca Cola": [], "Coco": [], "Cocoon": [], "COLORBLOCK": [], "Colorfone": [], "Competition Pro": [], "Computer Gear": [], "Connect It": [], "Connected Essentials": [], "Connect'Line": [], "Contour Design": [], "Cosonic": [], "Cougar": [], "COWIN": [], "crazybaby": [], "Cresyn Industrial": [], "CROSSCALL": [], "Crypto": [], "CRYSTAL AUDIO": [], "Cta": [], "Cubik": [], "Cyber Blue": [], "Cyber Snipa": [], "Cyborg": [], "Dacom": [], "DAMSON": [], "Datel": [], "Dectel": [], "Definitive": [], "Defunc": [], "DEGAUSS LABS": [], "deleyCON": [], "Delock": [], "Devia": [], "Dextra": [], "Dicota": [], "DIGITAL SILENCE": [], "DISNIX": [], "DIVACORE": [], "Doro": [], "Dotz": [], "DRAGON WAR": [], "Draxter": [], "Dreamgear": [], "Dymond": [], "EAMEY": [], "Earebel": [], "Earson": [], "EASARS": [], "EASYKADO": [], "Easytel": [], "Eblue": [], "E-BLUE": [], "ECE": [], "Echo": [], "E-Dimensional": [], "EERS": [], "ELESOUND": [], "Elipson": [], "ELITACCESS": [], "Elle": [], "Empire": [], "Emporia": [], "Encore": [], "Enjoy": [], "EPICGEAR": [], "Erato": [], "Ergenic": [], "Ericsson": [], "ESTUFF": [], "Eten": [], "ETIGER": [], "Everglide": [], "EVIL": [], "EVOLVEO": [], "Excel Com": [], "Expansys": [], "Exponent": [], "Facon": [], "FANTIME": [], "FASHION TALKY": [], "FEINTECH": [], "Fellowes": [], "Fff": [], "FIERRO": [], "Fiesta": [], "FINEBLUE": [], "FITBIT": [], "Fittek": [], "Flexus": [], "FLUOR": [], "Follow Up": [], "FONEMAX": [], "Fonex": [], "Fontastic": [], "Formosa": [], "Freaks & Geeks": [], "Free Style": [], "FREEGO": [], "FREEGUN": [], "Freemate": [], "FREESOUND": [], "Freewave": [], "FRENDS": [], "Fresh ‘n Rebel": [], "FUN CONNECTION": [], "Func": [], "Fundigital": [], "G.GEAR": [], "G.Skill": [], "GAMDIAS": [], "GAMEKRAFT": [], "Gameware": [], "Gamexpert": [], "GAVIO": [], "GBK": [], "Genesis": [], "GG Telecom": [], "Ggmm": [], "Gigaset": [], "Gioteck": [], "G-LAB": [], "Glofiish": [], "G-MOBILITY": [], "GN Netcom": [], "Golla": [], "GONBES": [], "Good Access": [], "GoSport": [], "GOUDISE": [], "GP": [], "Green": [], "Gsm": [], "GSound": [], "GT": [], "Guess": [], "HAC": [], "Hagenuk": [], "HANIZU": [], "HAPPY PLUGS": [], "Hds": [], "HIBLUE": [], "HIDITEC": [], "HIMADE": [], "Hi-Teh": [], "HMC": [], "HMDX Audio": [], "HOCO": [], "HONOR": [], "HOODIE BUDDIE": [], "HOUDT": [], "HSINI": [], "Hyperx": [], "I.AM+": [], "IBike": [], "ICANDY": [], "Ice Watch": [], "Icemat": [], "ICE-PHONE": [], "I-CREATION": [], "Idea": [], "Ideenwelt": [], "Ideus": [], "Idream": [], "IGGY POP": [], "IMAZE": [], "IMOOVE": [], "Impact": [], "inateck": [], "Indeca": [], "ING": [], "Inkclub": [], "Inline": [], "Interphone": [], "Iogear": [], "i-Paint": [], "ipipoo": [], "Ipone": [], "Iqua": [], "IS": [], "Isotech": [], "ISP": [], "IT7": [], "I-Tech": [], "IWILL": [], "JABEES": [], "JABLUE": [], "Jabra-Fake": [], "Jawbone": [], "Jelly Belly": [], "JPL": [], "Kanen": [], "Kaos": [], "Karade": [], "Kazimogo": [], "KEEKA": [], "KEEP OUT": [], "Kit": [], "Kitmobile": [], "KLIM": [], "Kondor": [], "KOTHAI": [], "kotion": [], "KREAFUNK": [], "KSIX": [], "Kworld": [], "Lanso": [], "LAPINETTE": [], "Laura Technology": [], "LDNIO": [], "Le Coq Sportif": [], "Leicke": [], "LEILING": [], "Levi`s": [], "LG-FAKE": [], "LIBRATONE": [], "LIONCAST": [], "Logic": [], "LOVELY@ME": [], "LUCID SOUND": [], "Luxa2": [], "Maas": [], "Mad Catz": [], "Maplin": [], "Marmitek": [], "MAROO": [], "MARS GAMING": [], "Martin Logan": [], "MARVO": [], "Maxon": [], "Maxwise": [], "MCA": [], "M-Cab": [], "Meizu": [], "METERS MUSIC": [], "MICROMOBILE": [], "MIIKEY": [], "Mini": [], "Mionix": [], "MIPOW": [], "Mipro": [], "Miq": [], "mitec": [], "Mitel": [], "Mitsubishi/Trium": [], "Mixcder": [], "Mizoo": [], "Mobil System": [], "Mobil Team": [], "Mobiland": [], "MOBILE TUNING": [], "Mobilize": [], "Mobisys": [], "Mocca Design": [], "Modelabs": [], "mojoburst": [], "MOLAMI": [], "Momodesign": [], "MOOSTER": [], "More": [], "MORUL": [], "MOSIDUN": [], "Mov": [], "MPOW": [], "Ms-Tech": [], "MTE": [], "Mtek": [], "MTT": [], "MTU": [], "Multimedia": [], "MUSIC SOUND": [], "mydoodah": [], "My-Extra": [], "NACON": [], "Naks": [], "Native Union": [], "Navroad": [], "NEKKER": [], "Nelyo": [], "Net Generation": [], "New Mobile": [], "Nextlink": [], "NOCS": [], "Noganet": [], "NOISEHUSH": [], "NOKIA MONSTER": [], "Nokia-Fake": [], "NOOSY": [], "Novero": [], "Nox": [], "N'Play": [], "Nuance": [], "Nueboo": [], "NUHEARA": [], "NX One": [], "Nxzen": [], "Nyko": [], "NZUP": [], "OAC": [], "OBLANC": [], "Odoyo": [], "OGLO": [], "Oke": [], "Omiz": [], "ONEDIRECT": [], "Orange": [], "ORB": [], "ORIGINAL FAKE": [], "Ovc": [], "Ovislink": [], "Ovleng": [], "OYKON": [], "Ozone": [], "Pama": [], "PATUOXUN": [], "PC Line": [], "PDP": [], "Pearl": [], "Perixx": [], "Peter Jäckel": [], "Philo": [], "Phone Team": [], "Pine": [], "PK": [], "Plantronics": [], "Platinet": [], "play2Run": [], "PLAYVISION": [], "PLUGGED": [], "PMR": [], "Pnx": [], "Point Kom": [], "POLEGAR": [], "Power A": [], "PowerCool": [], "Powerwalker": [], "PRECISION AUDIO": [], "PREMIUMCORD": [], "PRIF": [], "Pritech": [], "PROJECT SUSTAIN": [], "Promate": [], "PRS": [], "Pryma": [], "Pump Audio": [], "QCY": [], "Qoltec": [], "Q-pad": [], "Q-Sonic": [], "Qtek": [], "Qtrek": [], "Qumo": [], "RDI": [], "Rebeltec": [], "redlife": [], "REMAX": [], "Retrophone": [], "Richter": [], "Right": [], "Rix": [], "Roc": [], "Roccat": [], "Rock": [], "Rocketfish": [], "Roman": [], "S BOX": [], "SADES": [], "Salsa": [], "Samsonite": [], "Samsung-Fake": [], "Santok": [], "SATECHI": [], "SAVOX": [], "SBE": [], "SBS": [], "SEAWAG": [], "Seekas": [], "Sempre": [], "Sena": [], "Sendo": [], "SENSO": [], "Sep": [], "Setma Deltam": [], "SFR": [], "SGP": [], "Sharkoon": [], "SHOT CASE": [], "SINJI": [], "Sitecom": [], "Skech": [], "Skillkorp": [], "SKYLANDERS": [], "Smart TALK": [], "SMARTHAX": [], "Snap": [], "Snom": [], "Sofare": [], "Somic": [], "Soncm": [], "Sonim": [], "SONIXX": [], "Sony Ericsson": [], "Sony Ericsson-Fake": [], "Sony-Fake": [], "SoundPEATS": [], "Sounds": [], "SOUNDZ": [], "Southwing": [], "Soyt": [], "Spark": [], "Sparkle": [], "SPARTAN GEAR": [], "spectralink": [], "SPIRIT OF GAMER": [], "Sports": [], "Spydee": [], "Starline": [], "STEELPLAY": [], "STK": [], "STORM7": [], "Strax": [], "SUDIO": [], "SUNEN": [], "SUPERDRY": [], "Supertooth": [], "SWISS CHARGER": [], "SWISS MOBILE": [], "Swissvoice": [], "Syba": [], "SYSTEM-S": [], "TALIUS": [], "Talk Aloud": [], "TAMTAM": [], "TAOTRONICS": [], "Techair": [], "Techmade": [], "Techsolo": [], "Techtools": [], "TEKNISER": [], "Tektos": [], "Tekuni": [], "Telcom": [], "Teppaz": [], "TESORO": [], "THB Bury": [], "The Kase": [], "The Wand Company": [], "Thermaltake": [], "ThunderX3": [], "TIKOO": [], "Tiptel": [], "Tonino Lamborghini": [], "TOP": [], "Top Suxess": [], "Topcom": [], "Topp": [], "TOTU DESIGN": [], "Trade Invaders": [], "TRAINER": [], "TRANDS": [], "TRENDWOO": [], "Tritton": [], "TTLIFE": [], "Tucano": [], "Turtle Beach": [], "Twiins": [], "Twodots": [], "ubsound": [], "UCALL": [], "UIISII": [], "ultimate ears": [], "Under Control": [], "Union": [], "Uniq": [], "UNPLUG": [], "Urban Factory": [], "URBANISTA": [], "Us Blaster": [], "USAMS": [], "VAIN SOUND": [], "VENTION": [], "Veova": [], "Vespa": [], "VETTER": [], "VICTSING": [], "VIDVIE": [], "Viji": [], "Viking": [], "VULTECH": [], "VXI": [], "Wantek": [], "Wave": [], "Wave Concept": [], "WAYTEX": [], "WEARHAUS": [], "WESDAR": [], "WHATEVERITTAKES": [], "White Diamonds": [], "Wiko": [], "WILEYFOX": [], "WIRED-UP": [], "WOO": [], "WOOPSO": [], "Woozik": [], "Woxeo": [], "WTT": [], "X2": [], "XCSOURCE": [], "XD DESIGN": [], "XFX": [], "Xpower": [], "Xtech": [], "Xubix": [], "YADA": [], "Yarden": [], "YAYAGO": [], "Yealink": [], "Zaapa": [], "ZEALOT": [], "Zedem": [], "Zickplay": [], "Zipper": [], "ZOOOK": [], "ZOWIE": [], "Zucchetti": [], "Zykon": []},
      "c32669": {"AC Ryan": [], "Actidata": [], "Adaptec": [], "A-Data": [], "Addion": [], "ADLINK": [], "Agestar": [], "Akitio": [], "Allnet": [], "Alps": [], "Amacom": [], "AMD": [], "ANACOMDA": [], "ANGELBIRD": [], "Apacer": [], "Apache": [], "Apricorn": [], "Areca": [], "Argosy": [], "ASUSTOR": [], "Axiom": [], "Barracuda Networks": [], "Beghelli": [], "BIDUL": [], "BIPRA": [], "Biwin": [], "BLU-BASIC": [], "Blue Coat": [], "Bluemedia": [], "BOSTON": [], "BRINELL": [], "Cables Direct": [], "CCTV": [], "Check Point": [], "Chenbro": [], "Chieftec": [], "Clickfree": [], "Cloud": [], "CMS": [], "CnMemory": [], "Cometlabs": [], "CONNECTED DATA": [], "Connection": [], "Coskin": [], "CRU": [], "Crucial Technology": [], "Ctera": [], "D&S": [], "DAHUA": [], "Dane Elec": [], "Data Direct Network": [], "DATALOCKER": [], "Dawicontrol": [], "DESTROY POP": [], "Digittrade": [], "Disques Silice": [], "Dothill": [], "DROBO": [], "Durabook": [], "Easyraid": [], "Edimax": [], "Elgato": [], "EMC": [], "Energy": [], "Europart": [], "Exabyte": [], "Excelstor": [], "EXTERITY": [], "FUSiON-iO": [], "Geil": [], "Getac": [], "GOLD DIGITAL": [], "Golden Memory": [], "GOO": [], "Goodram": [], "G-Technology": [], "HGST": [], "HI-LEVEL": [], "HipDisk": [], "HITACHI DATA SYSTEMS": [], "HMB": [], "HORNETTEK": [], "Hyperdrive": [], "Hypertec": [], "I Storage": [], "I.NORYS": [], "Icy Dock": [], "Imation": [], "Infortrend": [], "Innodisk": [], "Integral": [], "Iocell": [], "Iomega": [], "ioSafe": [], "Ironkey": [], "ISO": [], "Jou Jye": [], "Kanex": [], "Kanguru": [], "Kentron": [], "KFA2": [], "King Elephant": [], "Kingmax": [], "KINGSPEC": [], "Kingston": [], "KLEVV": [], "Level One": [], "Lexar": [], "Leyio": [], "Linksys": [], "LONGSYS": [], "Lorca": [], "Lupus": [], "Maxtor": [], "Mc Afee": [], "MDT": [], "ME2": [], "MediaRange": [], "Memblaze": [], "Microcom": [], "Micron": [], "Micronet": [], "Microstorage": [], "Mitsumi": [], "Momobay": [], "Mophie": [], "Mpio": [], "Mtron": [], "Mushkin": [], "MX-Technology": [], "Nasdeluxe": [], "Netapp": [], "Newcom": [], "NewerTech": [], "Nexsan": [], "Nextodi": [], "NIMBLE STORAGE": [], "Novatech": [], "NOVATHINGS": [], "Ocz": [], "One Technologies": [], "Onnto": [], "Origin Storage": [], "Overland Storage": [], "OWC": [], "PANASAS": [], "Patriot Memory": [], "Perfectparts": [], "Pexagon": [], "Pikaone": [], "Planet": [], "Platinum": [], "Plextor": [], "PNY Technologies": [], "Promise": [], "PURE STORAGE": [], "QSAN TECHNOLOGY": [], "Quantum Corporation": [], "RAIDON": [], "Rapsody": [], "Riverbed": [], "Rixid": [], "RUBRIK": [], "Runcore": [], "Sandisk": [], "Seagate": [], "Seitec": [], "Silicon Power": [], "Silicon Systems": [], "Simpletech": [], "SK hynix": [], "Smartbuy": [], "Smartdisk": [], "SMC": [], "Snap Appliance": [], "SOLIDATA": [], "SOLIDFIRE": [], "Sonicwall": [], "Sonnet": [], "SONNICS": [], "SQP": [], "Stardom": [], "Startech": [], "sTec": [], "Storeva": [], "Storevault": [], "StorVision": [], "STREACOM": [], "Sun Microsystems": [], "Super Talent": [], "Symantec": [], "Synology": [], "Tanya Sarne": [], "Teamgroup": [], "TERRAMASTER": [], "THECUS": [], "TOP PERFORMANCE": [], "Travel Star": [], "Trendnet": [], "TVTECH": [], "V7": [], "Vantec": [], "VCE": [], "Veritas": [], "Vosonic": [], "Welland": [], "Western Scientific": [], "WHIPTAIL": [], "Xerom": [], "Ximeta": [], "Xiotech": [], "X-Micro": [], "XPG": [], "Xs Drive": [], "Xyratex": [], "Xystec": [], "ZAPPITI": [], "Zyxel": []},
      "c32683": {"Acco": [], "Adapt": [], "A-Rival": [], "Ask Proxima": [], "Avio": [], "Beambox": [], "BLUECAT": [], "Boxlight": [], "Christie": [], "CineVersum": [], "Crenova": [], "Davis": [], "Digital Projection": [], "Dream Vision": [], "Eiki": [], "Elmo": [], "E-Projex": [], "EVERLINE": [], "Fujix": [], "GOPICO": [], "I3": [], "iCodis": [], "INNOIO": [], "IPOWERUP": [], "JmGO": [], "Kindermann": [], "Liesegang": [], "LUXBURG": [], "Luximagen": [], "MediaLy": [], "Microvision": [], "Mili": [], "Mimio": [], "Miroir": [], "Nobo": [], "Optoma": [], "Phonica": [], "Puridea": [], "RIF6": [], "Runco": [], "SceneLights": [], "SHOPINNOV": [], "Sim2": [], "SIMPLEBEAM": [], "Starview": [], "Suant": [], "TECTECTEC": [], "UHAPPY": [], "Unic": [], "Unicview": [], "WowWee": [], "XSAGON": [], "Zte": []},
      "c32696": {"808": [], "8BITDO": [], "A Dece Oasis": [], "abit": [], "Aboutbatteries": [], "AC WORLDWIDE": [], "Acoustic Energy": [], "Acoustic Research": [], "Addon": [], "AIBIMY": [], "AKAI PROFESSIONAL": [], "Akios": [], "ALILO": [], "ALLOCACOC": [], "Altec": [], "AM-Denmark": [], "Amir": [], "Aml": [], "Ansmann": [], "Aodasen": [], "Apart": [], "Aq": [], "AQ AUDIO": [], "AQUAJAM": [], "Aquamusique": [], "Arkas": [], "Arowana": [], "Assmann": [], "ASWY": [], "Atake": [], "Audica": [], "Audio Tech": [], "AUDIOBOT": [], "Audioengine": [], "AUDYSSEY": [], "Auluxe": [], "AUTODRIVE": [], "AV CONCEPT": [], "Avanti": [], "AVS": [], "Awg": [], "AZATOM": [], "BASS EGG": [], "Beacon": [], "BEM": [], "Beqube": [], "BIJELA": [], "BINAURIC": [], "Blautel": [], "BLEE": [], "Boom": [], "BOOM BOTIX": [], "Born in France": [], "BOUNCE AUDIO": [], "Boynq": [], "BRAVEN": [], "B-SOUND": [], "Bull Audio": [], "BUNKERBOUND": [], "Burger": [], "BUZZEBIZZ": [], "Cabasse": [], "Cambridge Soundworks": [], "CAMINO": [], "CANNICE": [], "Canton": [], "CARBON AUDIO": [], "CaseGuru": [], "Cellux": [], "Chaumet": [], "CHOIIX": [], "Cimline": [], "Cirkuit": [], "Cjc": [], "Cml": [], "Comep": [], "Computer Sound": [], "Conran Audio": [], "Coppertech": [], "COUSOUND": [], "CRISTALRECORD": [], "Crono": [], "Crystal Speaker": [], "CUBELIGHT": [], "CuboQ": [], "Cuc": [], "Dali": [], "Dane Electronic": [], "DBEST": [], "D-Box": [], "Delux": [], "Dexlan": [], "Dexxa": [], "Diagram": [], "Diasonic": [], "DICE": [], "Digifocus": [], "Digital Inmotions Electronics": [], "DLH Energy": [], "Dmax Subtri": [], "Doss": [], "DOUPI": [], "Dr. Bott": [], "DREAMWAVE": [], "DRESZ": [], "DURALINE": [], "D-VICE": [], "Dynaudio": [], "EARISE": [], "EasyAcc": [], "E-Boda": [], "ebode": [], "Eclipse": [], "ECOXGEAR": [], "Edtasonic": [], "Electric Friends": [], "Electrojoe": [], "Elite": [], "emie": [], "EMOI": [], "en&is": [], "EPIKO": [], "Euro-10": [], "Ever Power": [], "Evestar": [], "Evidence Acoustics": [], "Ewoo": [], "Extel": [], "EZWAY": [], "F&d": [], "FADEDGE": [], "Fantasia": [], "FASHIONATION": [], "Fatechs": [], "Fenton": [], "FINITE ELEMENTE": [], "Fizz": [], "Force Media": [], "Franklin Electronic Publishers": [], "Fred & Friends": [], "FUGOO": [], "Fujitel": [], "FYDELITY": [], "Gameron": [], "Gamester": [], "GEAR HEAD": [], "GEAR IT": [], "GECHO": [], "Gecko": [], "GIMME TUNES": [], "GLOBAL GIZMOS": [], "Global Pad": [], "GO GROOVE": [], "GO ROCK": [], "GOAL ZERO": [], "Good Vision": [], "GOODIES": [], "GRACE DIGITAL": [], "Grayt Little Speaker": [], "Grohe": [], "G-Series": [], "Guillemot": [], "GVC": [], "HABY": [], "HCM": [], "HEADSOUND": [], "Hiro Corporation": [], "Homade": [], "Hurricane": [], "iBass": [], "iBlock": [], "IBM/Lenovo": [], "IBomb": [], "iBoutique": [], "ICE": [], "Ichona": [], "ICUTES": [], "Ik": [], "IKU": [], "ILE": [], "Imaingo": [], "IMIXID": [], "In2uit": [], "INCIDENCE": [], "Inkel": [], "Inno": [], "INNOVATEC": [], "INTENSE": [], "INVOXIA": [], "iriver": [], "iRock": [], "I-Rocks": [], "iSHOWER": [], "ISOTECH": [], "Istar": [], "Itamtam": [], "ITB Solution": [], "IUI": [], "Iwi": [], "Ixos": [], "JAMMIN PRO": [], "Jarre": [], "Jazz": [], "JBL Fake": [], "JBLAB": [], "Jnc": [], "JPW": [], "Juice": [], "Juster": [], "KAKKOII": [], "Kanto": [], "Kensington": [], "Klein und More": [], "K-Mex": [], "Koda": [], "Kores": [], "KRATOR": [], "Kt Tech.": [], "KUBXLAB": [], "La Chaise Longue": [], "Lars & Ivan": [], "Laser": [], "Lecci": [], "Ledwood": [], "Leitz": [], "Lemus": [], "LENRUE": [], "LEPA": [], "LEPOW": [], "LICK": [], "LIFEPROOF": [], "Lingo": [], "LINX": [], "Linx": [], "LITTLEBIGSOUND": [], "Logicool": [], "Lonsen": [], "LOTS": [], "Luckies": [], "LUMISKY": [], "Luxy Star": [], "Mac Audio": [], "Macrom": [], "MADISON": [], "MAGIC CLOUDS": [], "Maxi": [], "Maxview": [], "MEMORYSTAR": [], "MIGHTY BOOM BALL": [], "Miglia": [], "Mirage": [], "Miscella": [], "Mission": [], "MJS Technology": [], "Mobi": [], "MOBILITY ON BOARD": [], "Mobinote": [], "MOCCA": [], "MONSTERCUBE": [], "MOO": [], "MOOAS": [], "Morel": [], "MOVA": [], "MOVIO": [], "MR & MRS FRAGRANCE": [], "Mt Logic": [], "Munchkin": [], "MUSAIC": [], "MUSIBYTES": [], "Music angel": [], "MY AMP": [], "My Music": [], "Nakamichi": [], "NEW THEORY": [], "NILLKIN": [], "Nimzy": [], "Nippotec": [], "NJOY": [], "NOONDAY": [], "Northamber": [], "NPN": [], "Nubwo": [], "NUDEAUDIO": [], "NYNE": [], "OAXIS": [], "Officedata": [], "OLIVARY": [], "OMPERE": [], "ORA ÏTO": [], "Orbitsound": [], "Origaudio": [], "OSMOT ECO-LIGHT": [], "PADMATE": [], "PALADONE": [], "Palo Alto": [], "Patrick": [], "Paul Frank": [], "Paulmann": [], "PEAQ": [], "PERIPOWER": [], "Philippi": [], "Phonotonic": [], "Pickering": [], "pindo": [], "PIOU PIOU": [], "PIXMI": [], "PLOX": [], "PLUFY": [], "Podgear": [], "Podspeakers": [], "POWERMOVE": [], "PowerTraveller": [], "Primax": [], "Pulse": [], "Q Acoustics": [], "Qdos": [], "Qm": [], "Q-Tec": [], "RAIDFOX": [], "Raikko": [], "Ranex": [], "Ravonaudio": [], "RAWAUDIO": [], "Real Cable": [], "RED POSITIVE": [], "Re-Fuel": [], "RIVA AUDIO": [], "Rockfire": [], "Roth Audio": [], "ROXOBOX": [], "Saisho": [], "Scandyna": [], "Scythe": [], "SENGLED": [], "SIMPLE AUDIO": [], "SIYOUR": [], "SLIM PEARL": [], "SMARTAKUS": [], "sminno": [], "Smk": [], "SMOOZ": [], "SO SEVEN": [], "Sonic Impact": [], "Sound Asleep": [], "Sound Traveller": [], "Soundcast": [], "SOUNDCRUSH": [], "SOUNDLOGIC": [], "SOUNDS to go!": [], "Soundvision": [], "Soundyou": [], "Speakal": [], "Speck Products": [], "SPEEDMIND": [], "Spherex": [], "Spire": [], "Spongebob": [], "SPRACHT": [], "Square": [], "SSBRIGHT": [], "Stabo": [], "STELLE": [], "Studio Lab": [], "Sub Zero": [], "Suck UK": [], "Sunflex": [], "SUPER LEGEND": [], "Sveon": [], "SWISSTONE": [], "Tannoy": [], "TECNOSTYLE": [], "Thakral": [], "Think Outside": [], "Thonet & Vander": [], "Titanmedia": [], "Tonality": [], "Tooq": [], "Topdevice": [], "TOPSAIL": [], "TP-Link": [], "TRAIT TECH": [], "TREE-LABS": [], "TSST": [], "TSU:BEHÖ:A": [], "T-Visto": [], "Twelve South": [], "Twinmos": [], "TYLT": [], "uBoogie": [], "ULTRALINK": [], "United Labels": [], "Unomat": [], "UP SOUND": [], "Vers": [], "Vestalife": [], "VIBRA8": [], "VIBRASON": [], "Videologic": [], "Vifa": [], "VISION TOUCH": [], "Vitalup": [], "VOCOCAL": [], "Voix": [], "Wharfedale": [], "WHD": [], "WINK": [], "Wowee": [], "WOWTHEM": [], "WSTER": [], "XDREAM": [], "XENICS": [], "Xindao": [], "Xonic": [], "XOOPAR": [], "Xtrem": [], "Ye!!": [], "Yuppi Love Tech": [], "Zens": [], "Zeon": [], "Zignum": [], "ZOEETREE": [], "ZOOKA": []},
      "c32758": {"Amcor": [], "Audiovox": [], "Avmap": [], "Binatone": [], "Coyote": [], "Digma": [], "Domotix": [], "Dunlop": [], "ERLINYOU": [], "ESX": [], "Evensham": [], "Falk": [], "Geely": [], "Ifox": [], "IGN": [], "Kapsys": [], "Keomo": [], "Lowrance": [], "Magellan": [], "Magneti Marelli": [], "Mappy": [], "Memory-Map": [], "MGNav": [], "Munic": [], "Myguide": [], "Navgear": [], "Naviflash": [], "Navigon": [], "Navking": [], "Navman": [], "Ndrive": [], "Norauto": [], "Novogo": [], "Overland": [], "Peiying": [], "REPLICA": [], "Route 66": [], "SILIM": [], "SKP": [], "Smailo": [], "Snooper": [], "Sungoo": [], "VDO Dayton": [], "Viamichelin": [], "VORDON": [], "WIKANGO": [], "Witson": [], "Xetec": [], "X-Loc": [], "X-Road": [], "Xzent": []},
      "c32798": {"AtGames": [], "HYPERKIN": [], "Ouya": [], "Sega": [], "SNK": []},
      "c321272": {"Altimea": [], "Amoi": [], "Arena": [], "Aspects": [], "ATMT": [], "Audix": [], "AUNE": [], "Babysun": [], "Barthe": [], "Beat Sounds": [], "Bestlink": [], "Bluel": [], "BMS": [], "Bright": [], "Cayin": [], "Cebop": [], "Chic": [], "Cliod": [], "COLORFLY": [], "Dainet": [], "Deejay": [], "Diamond": [], "Digimania": [], "Digisette": [], "Digital Square": [], "Dolphin": [], "Dreameo": [], "EMATIC": [], "Emgeton": [], "ENMAC": [], "Exigo": [], "Exper": [], "Ezav": [], "Finis": [], "Frontier Labs": [], "Genx": [], "Gweilo": [], "Hango": [], "HIDIZS": [], "iAUDIO": [], "IKO": [], "Ingram": [], "Ioneit": [], "Iops": [], "Irok": [], "Ism Technologie": [], "Itronics": [], "Jazpiper": [], "KLIVER": [], "Lavod": [], "Live Music": [], "LOTOO": [], "Magic Star": [], "Mambo X": [], "MARGOUN": [], "Maxian": [], "Memory Power": [], "Microdia": [], "Mobiblu": [], "Mobilenote": [], "Monbeq": [], "Mpeye": [], "Muro": [], "Music Disk": [], "Muzio": [], "Mymemory": [], "Napa": [], "Netac": [], "New Tech": [], "Nextway": [], "Nomadeo": [], "Nomarque": [], "Nomatec": [], "Oasis": [], "Oracom": [], "Oricom": [], "Pacemaker": [], "Paxton": [], "Play on": [], "Pontis": [], "Pop3": [], "Powerman": [], "Questyle": [], "RCA": [], "RIO": [], "Rownsonic": [], "Rox": [], "Saehan": [], "Saytes": [], "Selar": [], "Seltronic": [], "Shanling": [], "SHIK": [], "Sonicblue": [], "Sylvania": [], "Synn": [], "Techmicro": [], "Tekeet": [], "Teknique": [], "TFD": [], "THE KUBE": [], "thebit": [], "Unicom": [], "Vusys": [], "Wmg": [], "Woodi": [], "Xelo": [], "Xen": [], "Xpert": [], "Yves Fely": []},
      "c321373": {"@TAB": [], "3Q": [], "4G Systems": [], "Ainol": [], "Aligator": [], "Allview": [], "ALPENTAB": [], "ALPIE TECHNOLOGY": [], "Apollo": [], "AQIPAD": [], "ARNOVA": [], "ARRENA": [], "ARTIZLEE": [], "ArtView": [], "Barnes&Noble": [], "BAUNZ": [], "Bebook": [], "BITMORE": [], "bq": [], "Cdip": [], "CDISPLAY": [], "Chicco": [], "Clarys Technolo": [], "CLUST": [], "Commax": [], "DF": [], "Dino": [], "DISCOVERY": [], "DPS": [], "Dyno": [], "EDERTIX": [], "Einstein": [], "Eken": [], "ESTAR": [], "E-STAR": [], "Evigroup": [], "Faktor Zwei": [], "FIREBRAND": [], "FONDI": [], "FOODLE": [], "FORCEBOOK": [], "GOTAB": [], "HDW": [], "Hitek": [], "I.ONIK": [], "IGET": [], "Ikon": [], "Ikonia": [], "INFINITON": [], "INNJOO": [], "IONIK": [], "Irbis": [], "IRULU": [], "Itel": [], "JMI": [], "Joyplus": [], "Ken Brown": [], "KLIPAD": [], "Kloner": [], "KOBO": [], "Konrow": [], "Lark": [], "LOGIC-INSTRUMEN": [], "Magalhaes": [], "MID": [], "Multipix": [], "Myaudio": [], "MYMAGA": [], "MYPAD": [], "Navon": [], "Nextbook": [], "No Name": [], "NOKIA (FI)": [], "Nordmende": [], "NOVATAB": [], "NVIDIA": [], "Nvsbl": [], "Onda": [], "ONYO": [], "Overmax": [], "Palit": [], "PANDIGITAL": [], "Papyre": [], "Phaser": [], "Pipo": [], "Pocketbook": [], "POSH": [], "POV": [], "Proscan": [], "QOOQ": [], "SKY-LABS": [], "SMARTAB": [], "SMARTAK": [], "Smartbook": [], "SQ": [], "Stanley Mobile": [], "START TABLET": [], "Super General": [], "Synchro": [], "Szenio": [], "TB TOUCH": [], "TECHNILINE": [], "Tecno": [], "Telecom": [], "TESLA": [], "Texet": [], "tolino": [], "Tom-Tec": [], "TOO": [], "TOUCHLET": [], "TOUGHSHIELD": [], "TURBOPAD": [], "ULTRA DIGITAL": [], "Unowhy": [], "UNUSUAL": [], "Vedia": [], "Versus": [], "Vexia": [], "Vido": [], "VINITY": [], "VIRTUAL": [], "Vodafone": [], "Wexler": [], "XIDO": [], "Xplore": [], "X-treme": [], "ZENITHINK": [], "Zero": [], "ZIF": [], "ZIPATO": []},
      "c329728": {"Asel": [], "Bella": [], "Bielmeier": [], "CASINO DELICES": [], "Chang Sheng Electrical": [], "Chef Master Kitchen": [], "COMFORTCOOK": [], "Cookworks": [], "Crafft": [], "CUSINIER DELUXE": [], "Doragrill": [], "DPE": [], "Durandal": [], "Elith": [], "Eltac": [], "Essential": [], "Forc": [], "Formido": [], "Galileo": [], "HOME ESSENTIALS": [], "Home-Tek": [], "Kasui": [], "Kdeo": [], "Kumtel": [], "Maister": [], "Newcook": [], "Roller/Grill": [], "SILVA HOMELINE": [], "Sirge": [], "Toyota": [], "Valory": [], "Vitrokitchen": [], "Vivalp": []},
      "c329801": {"Beer Supreme": [], "Bier Maxx": [], "Bier-Box": [], "Ezetil": [], "LA HOUBLONNIERE": [], "Mobicool": [], "Multidraft": [], "Tireuse": [], "Wunderbar": []}


    };
  

  $scope.Dic_Marque_tv =  ['Acer','Brandt','Essentialb','Finlux','Grundig','Haier','JVC','LG','Listo',
                           'Loewe','Muse','Panasonic','Philips','Polaroid','Proline','Reflexion','Samsung',
                           'Sharp','Shivaki','Smart Tech','Sony','Swedx','TCL','Telefunken','Thomson',
                           'Toshiba','Xoro'
                          ];
  $scope.Dic_Modeles_tv = [ '55 B7V','Bild 3.55 Oled','55C7V','Q8C','55C6V','55POS9002F','55POS901F',
                            'TX-55EZ950','KD-55A1','65C7V','KD-65ZD9','65E7V','TX-65EZ950','Bild 5.55',
                            '65B6V','KD-65A1','Bild 7.55','KD-75X9405C','TX-65EZ1000','65G6V','65W7',
                            '7.65','TX-65CZ950E','65EG960V','TX-65DX900','TX-58DX900E','65C6V','55B6V',
                            'KD-75ZD9','KD-100ZD9','UE40H6400','KD-55XE7005','KD-49XE9005','KD-55XE8505',
                            'TX-50CX700E','TX-55CX700E','U65C7006','KD-55XE9005','KD-65XE8505','KD-55XE9305',
                            'QE49Q7F','UE65KS8000','KD-65XE9005','QE55Q7F','KD-65XE9305','U75C7006','QE65Q7F',
                            'KD-75XE9005','QE65Q9F'
                          ];
  $scope.IndiceRefresh =  [ '100 Hz','1000 Hz','1100 Hz','1200 Hz','1300 Hz','1400 Hz','1500 Hz','1600 Hz',
                           '1700 Hz', '1800 Hz','1900 Hz', '200 Hz','2000 Hz','2100 Hz', '2200 Hz','2300 Hz',
                           '2400 Hz', '2500 Hz', '2600 Hz','300 Hz','3000 Hz', '400 Hz','50 Hz','500 Hz',
                           '60 Hz', '600 Hz','700 Hz','800 Hz','900 Hz'  
                          ];
  $scope.HDR =            [ 'HLG(LG TVs Only)' , 'HDR10' , 'Dolby Vision' ];
  $scope.Ratio =          [ '14:9' ,  '4:3' ,'16:9' ] ;
  $scope.Couleur =        [ 'Gris', 'Noir', 'Argent' , 'Blanc' ];
  $scope.PannelType =     ['PVA', 'IPS', 'VA'];
  $scope.FrameRate =      ['30p', '24p' , '50p' , '60p'];
  $scope.Design =         ['Incurve', 'Plat'];
  $scope.Energy =         ['A++', 'A', 'A+', 'B', 'C'];

  // ==================================== FROIDS LISTS ================================================//

  $scope.froids_type =       ['Réfrigérateur sans congélateur', 'Congélateur', 'Réfrigétateur combiné', 'Cave à vin'];

  $scope.froids_subtype   =  [''];
  $scope.froids_subtype_1 =  ['Standard','Compact'];
  $scope.froids_subtype_2 =  ['Armoire','Compact','Coffre'];
  $scope.froids_subtype_3 =  ['Américain','Congélateur en bas','Congélateur en haut','Compact'];
  $scope.froids_subtype_4 =  ['Service','Vieillissement','Multi-températures'];

  $scope.froids_hauteur    = ['30-75' , '75-100' , '100-120' , '120-160' , '160-180' , '180-195' , '195-205'];
  $scope.froids_largeur    = ['50-60', '60-70','70-80', '80-90', '90-105'];
  $scope.froids_profondeur = ['20-55', '55-60', '61-65', '66-75', 'Plus de 75'];

  $scope.froids_volume_0 =     ['Moins de 51', '51-140', '141-149', '150-179','180-259', 'Plus de 259'];
  // $scope.froids_volume_net =     ['Moins de 51', '51-140', '141-149', '150-179','180-259', 'Plus de 259'];
  $scope.froids_volume_1_0 =   ['Moins de 51', '51-140', '141-149', '150-179', '180-259', 'Plus de 259'];
  $scope.froids_volume_1_1 =   ['Moins de 150', '150-244', '245-273', '274-316', '317-425', 'Plus de 426'];
  $scope.froids_volume_2_and_3=['Moins de 200','200-299','300-400','Plus de 400'];


  $scope.froids_technologie_1       = ['No frost', 'Conventional'];

  $scope.froids_Stockage_3 =           ['Moins de 100', '100-200', 'Plus de 200'];


  $scope.froids_consommation = ['120-240','241-360','Plus de 360'];
  $scope.froids_posetype =     ['Pose libre','integrable'];
  $scope.froids_energy =       ['A++', 'A', 'A+', 'B', 'C','D'];
  $scope.froids_couleur =      ['Gris', 'Noir', 'Argent' , 'Blanc', 'Bleu', 'Beige', 'Jaune', 'Rouge', 'Vert','Creme', 'Marron', 'Orange', 'Rose', 'Or', 'Retro'];
  $scope.froids_system =       ['Statique' , 'Ventilé', 'Brassé'];

  // ==================================== TELEPHONES LISTS ================================================//

  $scope.telephones_system =     ['Android','Apple iOS','Windows Phone','BlackBerry','Autre'];

  $scope.telephones_resolution=["320x240","320x256","320x320","320x400","320x480","324x352","345x800","352x416","360x120","360x400","360x480","360x640","384x288","400x240","400x427","400x800","432x240","450x854","480x272","480x320","480x360","480x427","480x540","480x640","480x690","480x760","480x800","480x845","480x854","480x860","480x862","480x864","480x960","480x1024","540x960","600x800","600x1024","640x200","640x240","640x320","640x360","640x480","640x960","640x1136","720x720","720x1280","750x1334","768x1024","768x1280","800x352","800x480","800x600","800x1280","854x480","960x544","1024x480","1024x600","1080x1920","1200x1920","1220x1600","1280x768","1280x800","1366x768","1440x1440","1440x2560","1536x2048","1600x900","1920x1080","1920x1200","2048x2732","2160x3840","2560x1600"];

  $scope.telephones_memory =         ['4','8','16','...'];
  $scope.telephones_ram =            ['4','8','16','...'];
  $scope.telephones_cores =     ['1','2','4','6','8'];

  $scope.telephones_couleur =    ['Gris', 'Noir', 'Argent' , 'Blanc', 'Violet', 'Beige', 'Bleu', 'Or', 'Jaune', 'Orange', 'Rose', 'Rouge', 'Vert', 'Marron'];

// ==================================== LAPTOP LISTS ================================================//

 $scope.laptop_ram = ['1', '2', '3', '4', '6', '8', '12', '16', '20', '24', '32', '64'];
 $scope.laptop_cpu = ['Intel Core i7', 'Intel Core i5', 'Intel Core i3', 'Intel Core M', 'Intel Pentium', 'Intel Celeron', 'Intel Atom', 'AMD A-series', 'AMD E-series', 'AMD Fusion'];
 $scope.laptop_cpu_complete=["Intel Xeon E5-2648L v4 @ 1.80GHz","Intel Xeon E5-4648 v3 @ 1.70GHz","Intel Core i7-5950HQ @ 2.90GHz","Intel Xeon E3-1535M v6 @ 3.10GHz","Intel Xeon E3-1545M v5 @ 2.90GHz","Intel Core i7-7820HK @ 2.90GHz","Intel Core i7-4980HQ @ 2.80GHz","Intel Core i7-7920HQ @ 3.10GHz","Intel Core i7-4940MX @ 3.10GHz","Intel Core i7-4960HQ @ 2.60GHz","Intel Core i7-6920HQ @ 2.90GHz","Intel Core i7-6770HQ @ 2.60GHz","Intel Core i7-4930MX @ 3.00GHz","Intel Core i7-5850HQ @ 2.70GHz","Intel Core i7-4910MQ @ 2.90GHz","Intel Core i7-7820HQ @ 2.90GHz","Intel Core i7-4870HQ @ 2.50GHz","Intel Core i7-3940XM @ 3.00GHz","Intel Core i7-4860HQ @ 2.40GHz","Intel Xeon E3-1535M v5 @ 2.90GHz","Intel Core i7-3920XM @ 2.90GHz","Intel Core i7-6820HK @ 2.70GHz","Intel Core i7-4900MQ @ 2.80GHz","Intel Core i7-4850HQ @ 2.30GHz","Intel Core i7-7700HQ @ 2.80GHz","Intel Core i7-4770HQ @ 2.20GHz","Intel Core i7-3840QM @ 2.80GHz","Intel Core i7-6820EQ @ 2.80GHz","Intel Core i7-6820HQ @ 2.70GHz","Intel Core i7-4810MQ @ 2.80GHz","Intel Xeon D-1528 @ 1.90GHz","Intel Core i7-3820QM @ 2.70GHz","Intel Core i7-4800MQ @ 2.70GHz","Intel Core i7-5700HQ @ 2.70GHz","Intel Core i7-4760HQ @ 2.10GHz","Intel Core i7-3740QM @ 2.70GHz","Intel Core i7-4750HQ @ 2.00GHz","Intel Core i7-5700EQ @ 2.60GHz","Intel Core i7-3720QM @ 2.60GHz","Intel Core i7-6700HQ @ 2.60GHz","Intel Core i7-4722HQ @ 2.40GHz","Intel Core i7-4720HQ @ 2.60GHz","Intel Core i7-4710MQ @ 2.50GHz","Intel Core i7-4710HQ @ 2.50GHz","Intel Core i5-7440HQ @ 2.80GHz","Intel Core i7-4700HQ @ 2.40GHz","Intel Core i7-4700MQ @ 2.40GHz","Intel Core i7-4860EQ @ 1.80GHz","Intel Core i7-3630QM @ 2.40GHz","Intel Core i7-4702HQ @ 2.20GHz","Intel Core i7-4712HQ @ 2.30GHz","Intel Core i7-3610QM @ 2.30GHz","Intel Core i7-3615QM @ 2.30GHz","Intel Core i7-2960XM @ 2.70GHz","Intel Core i7-4712MQ @ 2.30GHz","Intel Core i7-3615QE @ 2.30GHz","Intel Core i7-4702MQ @ 2.20GHz","Intel Xeon E3-1505L v5 @ 2.00GHz","Intel Core i7-2920XM @ 2.50GHz","Intel Core i7-2860QM @ 2.50GHz","Intel Core i7-3632QM @ 2.20GHz","Intel Core i5-7300HQ @ 2.50GHz","Intel Core i7-3612QM @ 2.10GHz","Intel Core i7-2840QM @ 2.40GHz","Intel Core i5-6440HQ @ 2.60GHz","Intel Core i7-2820QM @ 2.30GHz","Intel Core i7-3635QM @ 2.40GHz","Intel Core i7-2760QM @ 2.40GHz","Intel Core i7-7567U @ 3.50GHz","Intel Core i7-6822EQ @ 2.00GHz","Intel Core i7-3610QE @ 2.30GHz","Intel Core i7-3612QE @ 2.10GHz","Intel Core i7-7660U @ 2.50GHz","Intel Core i7-2720QM @ 2.20GHz","Intel Core i5-7360U @ 2.30GHz","Intel Core i5-6300HQ @ 2.30GHz","Intel Core i7-7560U @ 2.40GHz","Intel Core i7-2670QM @ 2.20GHz","Intel Core i5-7260U @ 2.20GHz","Intel Core i5-6440EQ @ 2.70GHz","Intel Core i7-2710QE @ 2.10GHz","Intel Core i7-6567U @ 3.30GHz","Intel Core i7-7600U @ 2.80GHz","Intel Core i7-2630QM @ 2.00GHz","Intel Core i7-2675QM @ 2.20GHz","Intel Core i7-2635QM @ 2.00GHz","Intel Core i7-2715QE @ 2.10GHz","Intel Core i5-7267U @ 3.10GHz","Intel Core i7-7500U @ 2.70GHz","Intel Core i5-7300U @ 2.60GHz","Intel Core i5-6360U @ 2.00GHz","Intel Core i7-4610M @ 3.00GHz","Intel Core i7-5557U @ 3.10GHz","Intel Core i7-6650U @ 2.20GHz","Intel Core i5-6267U @ 2.90GHz","AMD FX-9830P","AMD Embedded R-Series RX-421BD","Intel Core i7-4600M @ 2.90GHz","Intel Core i7-6560U @ 2.20GHz","Intel Core i7-6600U @ 2.60GHz","Intel Core i5-4340M @ 2.90GHz","Intel Core i5-7200U @ 2.50GHz","Intel Core i7-3540M @ 3.00GHz","Intel Core i7-4578U @ 3.00GHz","Intel Core i5-5287U @ 2.90GHz","AMD FX-7600P APU","Intel Core i5-8250U @ 1.60GHz","Intel Core i7-6498DU @ 2.50GHz","AMD A12-9730P","Intel Core i5-4310M @ 2.70GHz","Intel Core i5-4330M @ 2.80GHz","Intel Core i5-4210H @ 2.90GHz","Intel Core i7-3520M @ 2.90GHz","AMD RX-427BB","Intel Core i7-6500U @ 2.50GHz","Intel Core i5-4288U @ 2.60GHz","Intel Core i5-3360M @ 2.80GHz","Intel Core i5-3380M @ 2.90GHz","Intel Core i5-4300M @ 2.60GHz","Intel Core i5-5257U @ 2.70GHz","Intel Core i5-6300U @ 2.40GHz","Intel Core i5-6260U @ 1.80GHz","Intel Core i5-4308U @ 2.80GHz","Intel Core i7-4558U @ 2.80GHz","Intel Core i7-4560U @ 1.60GHz","Intel Core i5-4278U @ 2.60GHz","Intel Core i7-5600U @ 2.60GHz","AMD PRO A12-9800B","Intel Core i3-4350T @ 3.10GHz","AMD A10-9630P","Intel Core i7-5550U @ 2.00GHz","Intel Core i5-3340M @ 2.70GHz","Intel Core i7-3687U @ 2.10GHz","Intel Core i5-4210M @ 2.60GHz","AMD PRO A12-8800B","Intel Core i7-5650U @ 2.20GHz","Intel Core i5-6198DU @ 2.30GHz","AMD FX-8800P","Intel Core i3-6100H @ 2.70GHz","Intel Core i7-3555LE @ 2.50GHz","AMD A12-9720P","Intel Core i5-4258U @ 2.40GHz","Intel Core i7-4600U @ 2.10GHz","AMD PRO A10-8730B","Intel Core i5-3320M @ 2.60GHz","AMD FX-9800P","AMD PRO A8-9600B","AMD FX-7600P","Intel Core i5-4200M @ 2.50GHz","Intel Core i7-4650U @ 1.70GHz","Intel Core i7-5500U @ 2.40GHz","Intel Core i5-6200U @ 2.30GHz","Intel Core i7-940XM @ 2.13GHz","Intel Core i7-3667U @ 2.00GHz","Intel Core i5-4402E @ 1.60GHz","Intel Core i7-4510U @ 2.00GHz","Intel Core i5-3230M @ 2.60GHz","Intel Core i7-2640M @ 2.80GHz","AMD PRO A8-8600B","Intel Core i3-4110M @ 2.60GHz","Intel Core i3-6100U @ 2.30GHz","Intel Core i3-7100U @ 2.40GHz","Intel Core i7-3537U @ 2.00GHz","AMD A10-9600P","Intel Core i7-2620M @ 2.70GHz","Intel Core i7-920XM @ 2.00GHz","Intel Core i3-6157U @ 2.40GHz","Intel Core i7-4550U @ 1.50GHz","Intel Core i5-3210M @ 2.50GHz","AMD A12-9700P","Intel Core i7-4500U @ 1.80GHz","Intel Core i3-6100E @ 2.70GHz","Intel Core i5-2540M @ 2.60GHz","Intel Core i5-5300U @ 2.30GHz","Intel Core i5-4300U @ 1.90GHz","Intel Core i5-3610ME @ 2.70GHz","Intel Core i5-7Y57 @ 1.20GHz","Intel Core i5-4310U @ 2.00GHz","Intel Core i3-5157U @ 2.50GHz","AMD A10-7400P","Intel Core m3-7Y30 @ 1.00GHz","AMD PRO A10-8700B","Intel Core i5-5250U @ 1.60GHz","Intel Core i5-3437U @ 1.90GHz","Intel Core i5-2510E @ 2.50GHz","Intel Core i5-4350U @ 1.40GHz","Intel Core i7-3517U @ 1.90GHz","Intel Core i5-2520M @ 2.50GHz","Intel Core i5-4260U @ 1.40GHz","Intel Core i5-7Y54 @ 1.20GHz","Intel Core i5-3427U @ 1.80GHz","Intel Core m3-7Y32 @ 1.10GHz","Intel Core m7-6Y75 @ 1.20GHz","Intel Core i5-5200U @ 2.20GHz","AMD A10-8700P","Intel Core i3-4100M @ 2.50GHz","Intel Core i5-4250U @ 1.30GHz","Intel Core i7-840QM @ 1.87GHz","Intel Core i5-2450M @ 2.50GHz","Intel Core i5-4210U @ 1.70GHz","Intel Core i3-3130M @ 2.60GHz","AMD A8-7200P","AMD A10-5750M APU","Intel Core m5-6Y54 @ 1.10GHz","Intel Core i5-2430M @ 2.40GHz","Intel Core i5-4200U @ 1.60GHz","Intel Core i5-2435M @ 2.40GHz","Intel Core m5-6Y57 @ 1.10GHz","AMD A8-8600P","AMD A10 PRO-7350B APU","Intel Core i7-3517UE @ 1.70GHz","Intel Core i7-820QM @ 1.73GHz","Intel Core i3-4000M @ 2.40GHz","Intel Core2 Quad Q9100 @ 2.26GHz","AMD FX-7500 APU","Intel Core i7-3689Y @ 1.50GHz","Intel Core i3-3120M @ 2.50GHz","Intel Core i5-3337U @ 1.80GHz","Intel Core i7-740QM @ 1.73GHz","Intel Core i7-2630UM @ 1.60GHz","Intel Pentium 4415U @ 2.30GHz","Intel Core i3-5020U @ 2.20GHz","Intel Atom C2758 @ 2.40GHz","Intel Core i5-2410M @ 2.30GHz","Intel Core i3-6006U @ 2.00GHz","AMD A10-4600M APU","Intel Core i5-3317U @ 1.70GHz","AMD A10-5757M APU","Intel Core i3-3110M @ 2.40GHz","Intel Core i3-5010U @ 2.10GHz","Intel Core m3-6Y30 @ 0.90GHz","Intel Core i3-4120U @ 2.00GHz","Intel Core M-5Y71 @ 1.20GHz","Intel Core i7-720QM @ 1.60GHz","Intel Core i3-5015U @ 2.10GHz","Intel Core i5-5350U @ 1.80GHz","Intel Core M-5Y70 @ 1.10GHz","AMD A8-5550M APU","Intel Pentium 4405U @ 2.10GHz","AMD A8-5557M APU","AMD A10-7300 APU","Intel Core i3-5005U @ 2.00GHz","Intel Core i7-2637M @ 1.70GHz","Intel Core i3-4158U @ 2.00GHz","AMD A10-4657M APU","Intel Core i3-4110U @ 1.90GHz","Intel Core i7-640M @ 2.80GHz","Intel Core i7-2677M @ 1.80GHz","Intel Core i3-2310E @ 2.10GHz","AMD PRO A4-3350B APU","AMD A8-7100 APU","Intel Core i3-4025U @ 1.90GHz","Intel Core M-5Y10c @ 0.80GHz","Intel Core i7-2617M @ 1.50GHz","AMD A10-5745M APU","Intel Core M-5Y31 @ 0.90GHz","Intel Core i3-2370M @ 2.40GHz","Intel Core i7-620M @ 2.67GHz","AMD A8 PRO-7150B APU","Intel Core M-5Y10 @ 0.80GHz","AMD A8-7410 APU","Intel Celeron G3900E @ 2.40GHz","Intel Core i3-4030U @ 1.90GHz","AMD Phenom II X940 Quad-Core","AMD A6-7310 APU","AMD A8-4500M APU","AMD Phenom II N830 3+1","Intel Core i5-2557M @ 1.70GHz","AMD Phenom II X920 Quad-Core","AMD A8-3550MX APU","Intel Core i5-580M @ 2.67GHz","AMD A9-9410","Intel Core i3-2350M @ 2.30GHz","Intel Core i3-2348M @ 2.30GHz","Intel Core i5-560M @ 2.67GHz","Intel Pentium 3825U @ 1.90GHz","AMD A10-4655M APU","AMD A8-5545M APU","Intel Core M-5Y51 @ 1.10GHz","Intel Core i7-610E @ 2.53GHz","AMD A8-6410 APU","Intel Core2 Quad Q9000 @ 2.00GHz","Intel Core i3-2330M @ 2.20GHz","Intel Core i3-2328M @ 2.20GHz","AMD A4-7210 APU","AMD PRO A6-8500B","AMD Phenom II N970 Quad-Core","AMD Phenom II N950 Quad-Core","Intel Core i3-4030Y @ 1.60GHz","Intel Core i7-2610UE @ 1.50GHz","AMD A4 PRO-3340B","Intel Core i3-4005U @ 1.70GHz","Intel Core i3-3227U @ 1.90GHz","AMD PRO A6-8530B","Intel Core i5-540M @ 2.53GHz","AMD A6-9220","Intel Core i3-4010U @ 1.70GHz","AMD GX-424CC SOC","Intel Core i3-2310M @ 2.10GHz","Intel Core i5-480M @ 2.67GHz","AMD A6-6310 APU","Intel Pentium 2030M @ 2.50GHz","AMD Embedded R-Series RX-216GD","AMD A6-5200 APU","AMD A8-3510MX APU","AMD A8-3530MX APU","AMD PRO A6-9500B","Intel Core i3-2332M @ 2.20GHz","Intel Core i3-2312M @ 2.10GHz","Intel Core i5-520M @ 2.40GHz","Intel Celeron 2000E @ 2.20GHz","Intel Core i5-460M @ 2.53GHz","Intel Core i5-2467M @ 1.60GHz","Intel Celeron 2970M @ 2.20GHz","Intel Pentium 3550M @ 2.30GHz","AMD GX-420CA SOC","Intel Core i3-3217U @ 1.80GHz","Intel Pentium 2020M @ 2.40GHz","AMD E2-7110 APU","AMD Phenom II N930 Quad-Core","Intel Core i5-4220Y @ 1.60GHz","Intel Pentium 3560M @ 2.40GHz","Intel Core i5-520 @ 2.40GHz","Intel Core i7-640LM @ 2.13GHz","Intel Celeron 1020E @ 2.20GHz","AMD A6-3430MX APU","AMD A9-9400","AMD Phenom II X620 Dual-Core","AMD A8-3520M APU","AMD A6-8500P","Intel Core i3-390M @ 2.67GHz","Intel Core i3-4012Y @ 1.50GHz","Intel Atom C2558 @ 2.40GHz","Intel Core i3-3217UE @ 1.60GHz","Intel Core2 Duo T9900 @ 3.06GHz","Intel Core M-5Y10a @ 0.80GHz","AMD A4-6210 APU","Intel Core2 Duo E8335 @ 2.93GHz","Intel Core2 Duo E8435 @ 3.06GHz","Intel Core i5-450M @ 2.40GHz","AMD A8-4555M APU","Intel Core i5-430M @ 2.27GHz","Intel Core i3-380M @ 2.53GHz","AMD Phenom II P960 Quad-Core","AMD A4-5050 APU","Intel Core i5-2537M @ 1.40GHz","AMD A9-9420","AMD A4-5100 APU","AMD A6-3410MX APU","Intel Pentium B980 @ 2.40GHz","Intel Pentium 4405Y @ 1.50GHz","Intel Celeron 2950M @ 2.00GHz","Intel Celeron 3765U @ 1.90GHz","Intel Core2 Extreme X9100 @ 3.06GHz","Intel Atom E3950 @ 1.60GHz","Intel Core2 Duo T9800 @ 2.93GHz","Intel Core i3-370M @ 2.40GHz","AMD A6-3420M APU","Intel Pentium N4200 @ 1.10GHz","Intel Core2 Duo P9700 @ 2.80GHz","AMD A6-9210","Intel Pentium 3805U @ 1.90GHz","AMD A8-7050","AMD A8-3500M APU","Intel Core i7-620LM @ 2.00GHz","Intel Pentium B970 @ 2.30GHz","AMD R-460L APU","Intel Pentium N3540 @ 2.16GHz","AMD Phenom II N870 Triple-Core","Intel Atom x7-Z8750 @ 1.60GHz","AMD GX-415GA SOC","Intel Core2 Duo E8235 @ 2.80GHz","AMD Phenom II N850 Triple-Core","Intel Core i3-330E @ 2.13GHz","Intel Core2 Duo T9600 @ 2.80GHz","AMD E2-9010","Intel Atom x7-Z8700 @ 1.60GHz","AMD A6-5350M APU","AMD A4-5000 APU","AMD A6-3400M APU","Intel Core i3-350M @ 2.27GHz","AMD E2-6110 APU","Intel Pentium N3530 @ 2.16GHz","AMD A6-5357M APU","Intel Core2 Extreme X9000 @ 2.80GHz","Intel Pentium N3710 @ 1.60GHz","AMD Phenom II N830 Triple-Core","AMD Phenom II P920 Quad-Core","Intel Core2 Duo P9600 @ 2.66GHz","Intel Atom x5-Z8550 @ 1.44GHz","Intel Pentium N3700 @ 1.60GHz","Intel Pentium B960 @ 2.20GHz","AMD E2-9000","AMD Phenom II N660 Dual-Core","Intel Celeron 1005M @ 1.90GHz","AMD A6 Micro-6500T APU","Intel Pentium 2127U @ 1.90GHz","Intel Core i3-2377M @ 1.50GHz","Intel Core2 Duo T9500 @ 2.60GHz","Intel Core i7-660UM @ 1.33GHz","Intel Core2 Duo E8335 @ 2.66GHz","AMD Phenom II P940 Quad-Core","Intel Celeron N3450 @ 1.10GHz","Intel Core2 Extreme X7800 @ 2.60GHz","Intel Pentium N3520 @ 2.16GHz","Intel Core2 Duo T9550 @ 2.66GHz","Intel Core i3-330M @ 2.13GHz","Intel Core2 Duo P9500 @ 2.53GHz","AMD A10 Micro-6700T APU","AMD A4-5150M APU","Intel Core i3-2375M @ 1.50GHz","Intel Celeron 3955U @ 2.00GHz","Intel Core2 Duo P9600 @ 2.53GHz","Intel Atom Z3795 @ 1.60GHz","Intel Core2 Duo E8135 @ 2.66GHz","AMD Phenom II P860 Triple-Core","Intel Core2 Duo P8800 @ 2.66GHz","Intel Celeron N2940 @ 1.83GHz","Intel Core2 Duo T9400 @ 2.53GHz","Intel Celeron 1037U @ 1.80GHz","AMD Phenom II N640 Dual-Core","AMD Phenom II P840 Triple-Core","Intel Celeron 3855U @ 1.60GHz","Intel Celeron B840 @ 1.90GHz","Intel Pentium B940 @ 2.00GHz","Intel Core i3-2340UE @ 1.30GHz","Intel Pentium B950 @ 2.10GHz","Intel Celeron 3215U @ 1.70GHz","Intel Pentium 3556U @ 1.70GHz","Intel Celeron 3755U @ 1.70GHz","Intel Core i3-2367M @ 1.40GHz","Intel Pentium 3558U @ 1.70GHz","Intel Celeron N3160 @ 1.60GHz","Intel Atom x5-Z8500 @ 1.44GHz","Intel Core i7-680UM @ 1.47GHz","Intel Celeron 3865U @ 1.80GHz","Intel Core2 Extreme X7900 @ 2.80GHz","AMD A4-4300M APU","AMD A6-7000","Intel Core2 Duo SP9400 @ 2.40GHz","AMD Phenom II N620 Dual-Core","Intel Celeron N3150 @ 1.60GHz","Intel Core i7-640UM @ 1.20GHz","AMD Turion II Ultra Dual-Core Mobile M640","Intel Core2 Duo T9300 @ 2.50GHz","Intel Core i3-2365M @ 1.40GHz","Intel Celeron 1000M @ 1.80GHz","Intel Core i5-560UM @ 1.33GHz","Intel Celeron 3205U @ 1.50GHz","Intel Pentium 2117U @ 1.80GHz","AMD QC-4000","Intel Celeron N2930 @ 1.83GHz","Intel Core2 Duo P8700 @ 2.53GHz","AMD A6-4400M APU","AMD E2-3800 APU","Intel Core2 Duo T7800 @ 2.60GHz","AMD Phenom II P820 Triple-Core","Intel Atom x5-E8000 @ 1.04GHz","Intel Pentium A1018 @ 2.10GHz","AMD Phenom II P650 Dual-Core","Intel Core2 Duo P9300 @ 2.26GHz","AMD Turion II N530 Dual-Core","Intel Core i3-2357M @ 1.30GHz","AMD R-260H APU","Intel Celeron 2981U @ 1.60GHz","Intel Celeron 2980U @ 1.60GHz","Intel Celeron 1017U @ 1.60GHz","AMD A6 PRO-7050B APU","AMD A4 Micro-6400T APU","Intel Core2 Duo P8600 @ 2.40GHz","Intel Pentium N3510 @ 1.99GHz","AMD Turion II Ultra Dual-Core Mobile M660","Intel Celeron B830 @ 1.80GHz","AMD A6-1450 APU","AMD Turion II N550 Dual-Core","Intel Core2 Duo P7550 @ 2.26GHz","Intel Celeron N2920 @ 1.86GHz","AMD Turion II P560 Dual-Core","AMD A6-5345M APU","Intel Core2 Duo T8300 @ 2.40GHz","AMD GX-412HC","Intel Celeron 2957U @ 1.40GHz","Intel Core2 Duo P8400 @ 2.26GHz","AMD TurionX2 Ultra DualCore Mobile ZM-85","Intel Celeron 2955U @ 1.40GHz","AMD Turion II P540 Dual-Core","Intel Core2 Duo P7570 @ 2.26GHz","Intel Celeron B820 @ 1.70GHz","Intel Core2 Duo P7450 @ 2.13GHz","AMD Turion II Ultra Dual-Core Mobile M620","Intel Core2 Duo T7700 @ 2.40GHz","AMD Turion II Ultra Dual-Core Mobile M600","Intel Celeron 1007U @ 1.50GHz","Intel Pentium P6300 @ 2.27GHz","Intel Core i5-540UM @ 1.20GHz","Intel Celeron B810 @ 1.60GHz","AMD Turion II Neo N54L Dual-Core","Intel Celeron B815 @ 1.60GHz","Intel Core2 Duo T6600 @ 2.20GHz","AMD Turion II P520 Dual-Core","Intel Core2 Duo T6670 @ 2.20GHz","VIA QuadCore L4700 @ 1.2+ GHz","Intel Core2 Duo T7600 @ 2.33GHz","Intel Core i5-520UM @ 1.07GHz","Intel Celeron P4600 @ 2.00GHz","AMD Turion X2 Ultra Dual-Core Mobile ZM-87","Intel Pentium P6200 @ 2.13GHz","Intel Pentium T4500 @ 2.30GHz","Intel Core i5-430UM @ 1.20GHz","Intel Core2 Duo L9600 @ 2.13GHz","Intel Pentium P6100 @ 2.00GHz","Intel Core i7-620UM @ 1.07GHz","AMD A4-3310MX APU","AMD Turion II Dual-Core Mobile M540","AMD Turion II Dual-Core Mobile M500","AMD Turion II Dual-Core Mobile M520","Intel Core2 Duo P7370 @ 2.00GHz","Intel Core2 Duo P7350 @ 2.00GHz","Intel Celeron 887 @ 1.50GHz","AMD E2-9000e","Intel Celeron 877 @ 1.40GHz","Intel Celeron B800 @ 1.50GHz","Intel Core2 Duo T8100 @ 2.10GHz","Intel Core2 Duo T6500 @ 2.10GHz","Celeron Dual-Core T3500 @ 2.10GHz","Intel Pentium T4400 @ 2.20GHz","AMD A6-4455M APU","AMD Turion X2 Ultra Dual-Core Mobile ZM-86","Intel Atom Z3775D @ 1.49GHz","Intel Core2 Duo T7500 @ 2.20GHz","Intel Pentium 3560Y @ 1.20GHz","Intel Core i5-470UM @ 1.33GHz","Intel Core2 Duo SL9400 @ 1.86GHz","Intel Core2 Duo T6570 @ 2.10GHz","Intel Atom Z3775 @ 1.46GHz","Intel Pentium P6000 @ 1.87GHz","AMD A4-3320M APU","Intel Core2 Duo T7400 @ 2.16GHz","Intel Atom Z3770 @ 1.46GHz","Intel Pentium T4300 @ 2.10GHz","AMD GX-222GC SOC","AMD Turion X2 Ultra Dual-Core Mobile ZM-85","AMD Turion X2 Dual-Core Mobile RM-77","Intel Core2 Duo T6400 @ 2.00GHz","Intel Pentium 987 @ 1.50GHz","AMD A4-3305M APU","Intel Celeron N2910 @ 1.60GHz","AMD A4-3330MX APU","AMD Turion X2 Ultra Dual-Core Mobile ZM-84","Intel Core2 Duo T5900 @ 2.20GHz","Celeron Dual-Core T3300 @ 2.00GHz","Intel Atom x5-Z8300 @ 1.44GHz","Intel Celeron 867 @ 1.30GHz","Intel Core2 Duo T7300 @ 2.00GHz","AMD A4-3300M APU","AMD Turion II Neo K685 Dual-Core","Intel Core2 Duo T5850 @ 2.16GHz","Celeron Dual-Core T3100 @ 1.90GHz","Intel Celeron 857 @ 1.20GHz","Intel Core i3-380UM @ 1.33GHz","Intel Core2 Duo T7200 @ 2.00GHz","AMD A4-4355M APU","Intel Celeron P4500 @ 1.87GHz","Intel Pentium T4200 @ 2.00GHz","AMD Turion 64 X2 Mobile TL-68","Intel Pentium 967 @ 1.30GHz","AMD Turion X2 Dual-Core Mobile RM-75","Intel Pentium 977 @ 1.40GHz","Intel Core2 Duo T5870 @ 2.00GHz","Intel Celeron N3350 @ 1.10GHz","Intel Core2 Duo U9600 @ 1.60GHz","AMD Turion 64 X2 Mobile TL-64","AMD Turion 64 X2 Mobile TL-66","AMD GX-218GL SOC","Intel Pentium T3400 @ 2.16GHz","AMD TurionX2 Dual Core Mobile RM-72","Intel Core2 Duo T5800 @ 2.00GHz","Intel Celeron 2961Y @ 1.10GHz","Intel Core2 Duo T7250 @ 2.00GHz","AMD GX-217GA SOC","AMD E2-3000M APU","Intel Pentium 957 @ 1.20GHz","AMD Turion 64 X2 Mobile TL-62","AMD Turion X2 Dual-Core Mobile RM-72","Intel Core2 Duo T5750 @ 2.00GHz","Celeron Dual-Core T3000 @ 1.80GHz","AMD E2-3000 APU","Intel Atom Z3745 @ 1.33GHz","Intel Core i3-330UM @ 1.20GHz","AMD Turion X2 Ultra Dual-Core Mobile ZM-82","Intel Atom x5-Z8350 @ 1.44GHz","Intel Atom Z3740 @ 1.33GHz","Intel Core2 Duo L9300 @ 1.60GHz","Intel Atom Z3745D @ 1.33GHz","Intel Celeron T1700 @ 1.83GHz","AMD Turion X2 Dual-Core Mobile RM-74","Intel Core2 Duo T5550 @ 1.83GHz","Intel Pentium 2129Y @ 1.10GHz","AMD Turion X2 Dual Core Mobile RM-76","AMD Athlon 64 X2 QL-65","Intel Atom x5-Z8330 @ 1.44GHz","Intel Pentium T3200 @ 2.00GHz","Intel Celeron 847E @ 1.10GHz","Intel Core2 Duo T5600 @ 1.83GHz","Intel Core Duo T2700 @ 2.33GHz","Intel Atom Z3740D @ 1.33GHz","AMD Athlon 64 X2 QL-62","AMD Turion Dual-Core RM-74","Intel Celeron N2840 @ 2.16GHz","AMD Turion X2 Ultra Dual-Core Mobile ZM-80","Intel Core2 Duo T7100 @ 1.80GHz","AMD Athlon 64 X2 QL-67","Intel Core2 Duo T5670 @ 1.80GHz","AMD Turion X2 Dual-Core Mobile RM-70","Intel Celeron P4505 @ 1.87GHz","AMD Turion 64 X2 Mobile TL-60","Intel Celeron N3060 @ 1.60GHz","AMD E1-7010 APU","AMD Athlon 64 X2 QL-64","AMD TurionX2 Dual Core Mobile RM-70","Intel Pentium U5600 @ 1.33GHz","AMD Turion II Neo K625 Dual-Core","Intel Core2 Duo L7700 @ 1.80GHz","Intel Celeron N3010 @ 1.04GHz","AMD Turion Dual-Core RM-75","Intel Atom C2358 @ 1.74GHz","Intel Celeron N2820 @ 2.13GHz","AMD E1 Micro-6200T APU","Intel Core2 Duo L7500 @ 1.60GHz","Intel Celeron N2830 @ 2.16GHz","AMD Turion 64 X2 Mobile TL-58","AMD Athlon 64 X2 QL-66","Intel Core Duo T2600 @ 2.16GHz","Intel Pentium T2390 @ 1.86GHz","AMD Turion X2 Dual Core Mobile RM-70","Intel Celeron 847 @ 1.10GHz","Intel Core2 Duo SU9400 @ 1.40GHz","Intel Celeron N2808 @ 1.58GHz","Intel Core2 Duo T5300 @ 1.73GHz","Intel Celeron T1600 @ 1.66GHz","Intel Atom Z3735E @ 1.33GHz","AMD Athlon 64 X2 QL-60","Intel Core2 Duo T5500 @ 1.66GHz","Intel Atom Z3736F @ 1.33GHz","AMD Turion II Neo N40L Dual-Core","Intel Atom Z3735D @ 1.33GHz","Intel Atom Z3735G @ 1.33GHz","Intel Atom Z3735F @ 1.33GHz","Intel Celeron N3000 @ 1.04GHz","Intel Core2 Duo T5470 @ 1.60GHz","Intel Core2 Duo T5450 @ 1.66GHz","Intel Atom C2338 @ 1.74GHz","AMD Turion Dual-Core RM-70","AMD E1-6015 APU","AMD E1-2500 APU","Intel Celeron N3050 @ 1.60GHz","AMD Turion 64 X2 Mobile TL-56","Intel Core Duo T2500 @ 2.00GHz","Intel Core2 Duo U7300 @ 1.30GHz","AMD Turion X2 Dual Core L510","Intel Pentium SU4100 @ 1.30GHz","Intel Celeron N2815 @ 1.86GHz","Intel Core2 Duo U9300 @ 1.20GHz","AMD Athlon II Neo K345 Dual-Core","Intel Celeron N2807 @ 1.58GHz","Intel Atom E3827 @ 1.74GHz","AMD E1-6010 APU","Intel Core2 Duo L7400 @ 1.50GHz","Intel Pentium T2370 @ 1.73GHz","Intel Core Duo T2450 @ 2.00GHz","Intel Core2 Duo L7300 @ 1.40GHz","AMD Turion Dual-Core RM-72","Intel Pentium U5400 @ 1.20GHz","Intel Core2 Duo T5200 @ 1.60GHz","Intel Pentium T2330 @ 1.60GHz","Intel Core2 Duo T5250 @ 1.50GHz","AMD E2-2000 APU","Intel Core2 Duo T5270 @ 1.40GHz","AMD Athlon II Neo N36L Dual-Core","AMD Turion Neo X2 Dual Core L625","Intel Celeron B720 @ 1.70GHz","Intel Atom x5-E3930 @ 1.30GHz","Intel Atom Z3770D @ 1.49GHz","Intel Celeron U3600 @ 1.20GHz","Intel Core Duo T2400 @ 1.83GHz","AMD G-T56N","Intel Celeron SU2300 @ 1.20GHz","AMD Athlon II Neo K325 Dual-Core","Intel Celeron N2806 @ 1.60GHz","Intel Celeron N2810 @ 2.00GHz","AMD E-450 APU","AMD E1-2200 APU","AMD Turion 64 X2 Mobile TL-52","Intel Core Duo T2350 @ 1.86GHz","Intel Core Duo T2250 @ 1.73GHz","AMD G-T56E","Intel Celeron 807 @ 1.50GHz","AMD Turion 64 X2 Mobile TL-50","AMD GX-212JC SOC","Intel Core Duo T2300 @ 1.66GHz","Intel Core Duo L2500 @ 1.83GHz","Intel Celeron U3400 @ 1.07GHz","Intel Core2 Duo L7100 @ 1.20GHz","Intel Pentium T2310 @ 1.46GHz","Intel Atom D2701 @ 2.13GHz","AMD G-T48E","Intel Pentium T2080 @ 1.73GHz","Intel Core2 Duo U7700 @ 1.33GHz","Intel Pentium T2130 @ 1.86GHz","Intel Core Duo L2400 @ 1.66GHz","Intel Celeron 925 @ 2.30GHz","AMD E1-1500 APU","Intel Celeron U3405 @ 1.07GHz","Intel Core2 Duo L7200 @ 1.33GHz","AMD V160","Intel Pentium T2060 @ 1.60GHz","AMD E1-1200 APU","Intel Core2 Duo U7600 @ 1.20GHz","VIA Nano L3600@2000MHz","AMD V140","AMD A4-1200 APU","AMD V120","AMD E1-2100 APU","Intel Atom N2800 @ 1.86GHz","AMD Turion 64 Mobile ML-42","AMD E-300 APU","Intel Celeron 827E @ 1.40GHz","AMD A4-1250 APU","VIA Nano X2 U4025 @ 1.2 GHz","AMD Turion 64 Mobile ML-44","VIA Nano L3050@1800MHz","Intel Core2 Duo U7500 @ 1.06GHz","Intel Atom N570 @ 1.66GHz","Mobile AMD Athlon 64 4000+","AMD Sempron M120","Mobile AMD Athlon XP","Intel Atom Z2760 @ 1.80GHz","Intel Core Duo U2400 @ 1.06GHz","AMD Athlon II Neo K145","Intel Celeron M 540 @ 1.86GHz","AMD Turion 64 Mobile MT-40","Intel Celeron 560 @ 2.13GHz","Intel Atom N2600 @ 1.60GHz","Intel Celeron 570 @ 2.26GHz","AMD Turion 64 Mobile ML-40","Intel Atom N550 @ 1.50GHz","Mobile AMD Sempron 3800+","VIA Nano L3025@1600MHz","AMD G-T40N","Intel Core Duo U2500 @ 1.20GHz","AMD Turion 64 Mobile MK-38","Mobile AMD Athlon XP-M","Mobile AMD Athlon 64 3400+","Intel Celeron 540 @ 1.86GHz","Intel Pentium M 2.13GHz","Intel Pentium M 2.26GHz","Mobile AMD Athlon XP-M (LV)","Mobile AMD Athlon XP-M (LV) 3200+","VIA Nano U3100 (1.6GHz Capable)","Intel Celeron 550 @ 2.00GHz","Mobile AMD Athlon MP-M 2800+","Intel Atom E3826 @ 1.46GHz","Mobile AMD Athlon XP-M 3200+","AMD G-T40E","AMD Z-60 APU","AMD Turion 64 Mobile MT-37","Mobile Intel Pentium 4 3.46GHz","Mobile AMD Athlon XP-M (LV) 2800+","AMD Athlon II Neo K125","Intel Core Solo T1400 @ 1.83GHz","Intel Celeron 530 @ 1.73GHz","Intel Core2 Solo U3500 @ 1.40GHz","AMD Turion 64 Mobile MK-36","Intel Pentium M 2.00GHz","AMD C-50","Intel Celeron M 530 @ 1.73GHz","Intel Celeron M 723 @ 1.20GHz","Intel Celeron N2805 @ 1.46GHz","Intel Celeron M 450 @ 2.00GHz","AMD Sempron SI-42","Mobile AMD Athlon 64 3000+","Intel Pentium M 2.10GHz","Mobile AMD Athlon 64 3200+","AMD Turion 64 Mobile ML-37","Mobile AMD Sempron 3300+","Mobile AMD Sempron 3400+","Mobile AMD Athlon 64 2800+","Mobile AMD Athlon XP-M 3100+","Intel Pentium M 1.86GHz","Mobile Intel Pentium 4 3.33GHz","AMD Sempron SI-40","Mobile AMD Athlon 64 3700+","Intel Celeron M 520 @ 1.60GHz","AMD Turion 64 Mobile MT-34","Mobile AMD Sempron 3600+","VIA Nano L2100@1800MHz","AMD Turion 64 Mobile MT-32","Intel Celeron 743 @ 1.30GHz","AMD Turion 64 Mobile ML-34","AMD Turion 64 Mobile MT-28","Mobile AMD Sempron 3100+","Intel Core2 Solo U3300 @ 1.20GHz","Intel Pentium M 1.73GHz","Intel Celeron M 440 @ 1.86GHz","Intel Pentium M 1.70GHz","Mobile AMD Sempron 3500+","AMD Turion 64 Mobile ML-32","VIA Nano U3300@1200MHz","Intel Celeron 723 @ 1.20GHz","Intel Pentium SU2700 @ 1.30GHz","Intel Pentium M 1.80GHz","AMD Turion 64 Mobile ML-30","Intel Core Solo T1350 @ 1.86GHz","AMD GX-210JA SOC","Mobile AMD Athlon 64 2700+","Intel Core Solo T1300 @ 1.66GHz","Mobile AMD Sempron 2600+","Intel Celeron M 1.70GHz","AMD Turion 64 Mobile ML-28","Mobile AMD Sempron 3000+","Intel Atom Z550 @ 2.00GHz","VIA Nano L2007@1600MHz","AMD Turion 64 Mobile MT-30","Mobile AMD Athlon MP-M 2000+","VIA Nano U2250 (1.6GHz Capable)","Intel Pentium M 1700MHz","Mobile AMD Athlon XP-M (LV) 2200+","Mobile AMD Athlon 2500+","Mobile AMD Athlon XP-M 2600+","Intel Celeron 807UE @ 1.00GHz","Intel Celeron M 430 @ 1.73GHz","Intel Pentium M 1.50GHz","Intel Pentium M 1.60GHz","Intel Celeron M 1.60GHz","Mobile AMD Athlon XP-M 2800+","Mobile AMD Athlon XP-M 3000+","Mobile AMD Athlon XP-M 2200+","Mobile AMD Athlon 4 2400+","Mobile AMD Sempron 2800+","Intel Pentium M 1500MHz","Mobile AMD Sempron 3200+","Mobile AMD Athlon XP-M 2500+","Intel Atom Z540 @ 1.86GHz","Intel Celeron M 1.50GHz","Mobile AMD Athlon XP-M 2400+","Intel Pentium M 1.40GHz","Intel Pentium M 1600MHz","Mobile AMD Athlon XP-M 1900+","Intel Celeron M 420 @ 1.60GHz","Mobile AMD Athlon XP-M (LV) 2000+","Intel Celeron M 1500MHz","Intel Core Solo U1500 @ 1.33GHz","Intel Celeron M 360 1.40GHz","Mobile AMD Athlon XP-M 1700+","Intel Celeron 215 @ 1.33GHz","Intel Pentium M 1400MHz","AMD E-240","Intel Celeron M 410 @ 1.46GHz","Intel Celeron M 1.30GHz","Intel Atom N475 @ 1.83GHz","Mobile AMD Athlon 4","Mobile Intel Pentium 4 - M 2.60GHz","Mobile AMD Athlon XP-M 1800+","Intel Core2 Solo U2200 @ 1.20GHz","AMD C-30","Intel Atom N2100 @ 1.60GHz","Mobile Intel Celeron 1333MHz","Intel Atom N470 @ 1.83GHz","VIA Nano U2500@1200MHz","AMD G-T52R","Intel Celeron M 1300MHz","Intel Core2 Solo U2100 @ 1.06GHz","Intel Pentium M 1300MHz","Intel Pentium M 1.30GHz","Mobile AMD Athlon XP-M 2000+","Intel Atom N450 @ 1.66GHz","Mobile AMD Athlon XP-M (LV) 1600+","VIA Nano L2207@1600MHz","Mobile AMD Athlon MP-M 2400+","Mobile Intel Celeron 1200MHz","Mobile Intel Pentium III - M 1133MHz","Mobile Intel Pentium III - M 1333MHz","Mobile AMD Athlon XP-M (LV) 1500+","Intel Atom N280 @ 1.66GHz","Intel Atom N455 @ 1.66GHz","Intel Core Solo U1400 @ 1.20GHz","Intel Atom Z530 @ 1.60GHz","Mobile Intel Celeron 2.50GHz","Mobile Intel Pentium 4 2.30GHz","Intel Core Solo U1300 @ 1.06GHz","VIA Nano U3500@1000MHz","AMD V105","VIA Nano U2250@1300+MHz","Intel Atom E660 @ 1.30GHz","Intel Atom N270 @ 1.60GHz","Intel Pentium III Mobile 1066MHz","Mobile AMD Athlon 1400+","Mobile AMD Athlon MP-M 1800+","Mobile Intel Pentium III - M 1200MHz","Intel Pentium III Mobile 1200MHz","Mobile AMD Athlon XP-M 1500+","Intel Pentium M 1100MHz","Mobile AMD Athlon XP-M 1600+","Mobile Intel Pentium 4 - M 2.50GHz","Intel Celeron M 443 @ 1.20GHz","Mobile AMD Sempron 2100+","Intel Pentium III Mobile 1133MHz","Mobile Intel Pentium III - M 1000MHz","Intel Atom Z670 @ 1.50GHz","Intel Pentium III Mobile 1000MHz","Mobile Intel Celeron 2.40GHz","Intel Pentium M 1200MHz","Intel Pentium M 1000MHz","Mobile Intel Pentium 4 - M 1.90GHz","AMD G-T44R","Mobile Intel Celeron 2.20GHz","Intel Pentium M 900MHz","Intel Atom Z515 @ 1.20GHz","Intel Pentium III Mobile 933MHz","Intel Atom Z520 @ 1.33GHz","Mobile Intel Pentium 4 - M 2.40GHz","Mobile Intel Pentium III - M 866MHz","Intel Pentium 4 Mobile 1.90GHz","Mobile Intel Pentium 4 - M 2.20GHz","Intel Pentium 4 Mobile 1.70GHz","Intel Celeron M 1.00GHz","Intel Celeron M 900MHz","Mobile Intel Celeron 2.00GHz","Intel Pentium 4 Mobile 2.00GHz","Mobile Intel Pentium 4 - M 2.00GHz","Mobile Intel Pentium III - M 933MHz","Intel Pentium 4 Mobile 1.50GHz","Mobile Intel Pentium 4 - M 1.60GHz","Intel Atom Z510 @ 1.10GHz","Mobile Intel Celeron 1.50GHz","Mobile Intel Celeron 1.60GHz","Intel Celeron B710 @ 1.60GHz","Mobile Intel Celeron 1.80GHz","Mobile Intel Pentium 4 - M 1.80GHz","Intel Celeron M ULV 800MHz","Mobile AMD Athlon XP-M 1400+","VIA C7-M 1600MHz","Intel Pentium III Mobile 800MHz","Mobile Intel Celeron 1.70GHz","Intel Pentium 4 Mobile 1.60GHz","Intel Pentium 4 Mobile 1.80GHz","Mobile Intel Pentium 4 - M 1.70GHz","Mobile Intel Celeron 1.20GHz","VIA C7-M 1000MHz","Intel Pentium III Mobile 866MHz","Intel Celeron M 600MHz","Intel Pentium 4 Mobile 1.40GHz","Intel Pentium III Mobile 750MHz"];
 $scope.laptop_gpu_complete=["128 DDR Radeon 9700 TX w/TV-Out","128MB DDR Radeon 9800 Pro","128MB RADEON X600 SE","256MB RADEON X600","7900 MOD - Radeon HD 6520G","A6 Micro-6500T Quad-Core APU with RadeonR4","ABIT Siluro T400","ALL-IN-WONDER 9000","ALL-IN-WONDER RADEON 8500DV","All-in-Wonder X1900","ALL-IN-WONDER X800 GT","ASUS EAH4870x2","Barco MXRT 5400","Barco MXRT 5450","Chell 1.7b for Intel 945G","Chell 1.7b for Intel G33/G31","Chell 1.7b for Mobile Intel 945","Chell 1.8a for Mobile Intel 965","Chell 1.8b for Intel 945G","Chell 1.8b for Intel G33/G31","Chell 1.8b for Mobile Intel 945","Chell 1.8b for Mobile Intel 965","Chipset Intel G41 Express","Device","EAH6450","Famille de jeu de puces Express Intel 946GZ","FireGL X1","FireMV 2250","FirePro 2260","FirePro M4000 Mobility Pro","FirePro M40003","FirePro M4150","FirePro M4170","FirePro M6000 Mobility Pro","FirePro S7150","FirePro V4800","FirePro V7000 Adapter","FirePro V9800 Adapter","FirePro W4100 Adapter","FirePro W4170M","Firepro W4190M","FirePro W5130M","Firepro W5170M","FirePro W7000 Adapter","FirePro W7100 Adapter","FirePro W7170M","FirePro W8000 Adapter","FirePro W8100 Graphic Adapter","nVidia Geforce 256","nVidia Geforce 305M","nVidia Geforce 310M","nVidia Geforce 315M","nVidia Geforce 320M","nVidia Geforce 405","nVidia Geforce 410M","nVidia Geforce 505","nVidia Geforce 605","nVidia Geforce 6100","nVidia Geforce 6100 nForce 400","nVidia Geforce 6100 nForce 405","nVidia Geforce 6100 nForce 420","nVidia Geforce 6100 nForce 430","nVidia Geforce 610M","nVidia Geforce 615","nVidia Geforce 6150","nVidia Geforce 6150 LE","nVidia Geforce 6150SE","nVidia Geforce 6150SE nForce 430","nVidia Geforce 6200 TurboCache","nVidia Geforce 6200SE TurboCache","nVidia Geforce 6610 XL","nVidia Geforce 6700 XL","nVidia Geforce 7000M","nVidia Geforce 7000M / nForce 610M","nVidia Geforce 7025 / nForce 630a","nVidia Geforce 7050 / nForce 610i","nVidia Geforce 7050 / nForce 620i","nVidia Geforce 7050 / nForce 630i","nVidia Geforce 7050 PV / nForce 630a","nVidia Geforce 705M","nVidia Geforce 7100 / nForce 630i","nVidia Geforce 710A","nVidia Geforce 710M","nVidia Geforce 7150 / nForce 630i","nVidia Geforce 7150M / nForce 630M","nVidia Geforce 7300 SE/7200 GS","nVidia Geforce 730A","nVidia Geforce 7350 LE","nVidia Geforce 7650 GS","nVidia Geforce 800A","nVidia Geforce 800M","nVidia Geforce 8100 / nForce 720a","nVidia Geforce 810A","nVidia Geforce 810M","nVidia Geforce 8200","nVidia Geforce 8200M G","nVidia Geforce 820A","nVidia Geforce 820M","nVidia Geforce 825M","nVidia Geforce 8300","nVidia Geforce 830A","nVidia Geforce 830M","nVidia Geforce 8400","nVidia Geforce 8400 SE","nVidia Geforce 8400M G","nVidia Geforce 8400M GS","nVidia Geforce 8400M GT","nVidia Geforce 840A","nVidia Geforce 840M","nVidia Geforce 845M","nVidia Geforce 8600GS","nVidia Geforce 8600M GS","nVidia Geforce 8600M GT","nVidia Geforce 8700M GT","nVidia Geforce 8800M GTS","nVidia Geforce 8800M GTX","nVidia Geforce 9100","nVidia Geforce 9100M G","nVidia Geforce 910M","nVidia Geforce 9200","nVidia Geforce 9200M GE","nVidia Geforce 9200M GS","nVidia Geforce 920A","nVidia Geforce 920M","nVidia Geforce 920MX","nVidia Geforce 9300","nVidia Geforce 9300 / nForce 730i","nVidia Geforce 9300GE","nVidia Geforce 9300M G","nVidia Geforce 9300M GS","nVidia Geforce 930A","nVidia Geforce 930M","nVidia Geforce 930MX","nVidia Geforce 9400","nVidia Geforce 9400M","nVidia Geforce 9400M G","nVidia Geforce 940A","nVidia Geforce 940M","nVidia Geforce 940MX","nVidia Geforce 945M","nVidia Geforce 9500 GS","nVidia Geforce 9500M","nVidia Geforce 9500M G","nVidia Geforce 9500M GS","nVidia Geforce 9600M GS","nVidia Geforce 9600M GT","nVidia Geforce 9600M GT / nVidia Geforce GT 220M","nVidia Geforce 9650M GS","nVidia Geforce 9650M GT","nVidia Geforce 9700M GT","nVidia Geforce 9700M GTS","nVidia Geforce 9800 GTX/9800 GTX+","nVidia Geforce 9800 S","nVidia Geforce 9800M GS","nVidia Geforce 9800M GT","nVidia Geforce 9800M GTS","nVidia Geforce 9800M GTX","nVidia Geforce FX 5200LE","nVidia Geforce FX 5200SE","nVidia Geforce FX 5600XT","nVidia Geforce FX Go 5200","nVidia Geforce FX Go 5600","nVidia Geforce FX Go5300","nVidia Geforce FX Go5650","nVidia Geforce FX Go5700","nVidia Geforce G 103M","nVidia Geforce G 105M","nVidia Geforce G100","nVidia Geforce G102M","nVidia Geforce G105M","nVidia Geforce G200","nVidia Geforce G205M","nVidia Geforce G210","nVidia Geforce G210M","nVidia Geforce Go 6100","nVidia Geforce Go 6150","nVidia Geforce Go 6200","nVidia Geforce Go 6400","nVidia Geforce Go 6600","nVidia Geforce Go 6600 TE/6200 TE","nVidia Geforce Go 6800","nVidia Geforce Go 6800 Ultra","nVidia Geforce Go 7200","nVidia Geforce Go 7300","nVidia Geforce Go 7400","nVidia Geforce Go 7600","nVidia Geforce Go 7600 GT","nVidia Geforce Go 7700","nVidia Geforce Go 7800","nVidia Geforce Go 7800 GTX","nVidia Geforce Go 7900 GS","nVidia Geforce Go 7950 GTX","nVidia Geforce GPU","nVidia Geforce GT 120M","nVidia Geforce GT 130M","nVidia Geforce GT 220M","nVidia Geforce GT 230","nVidia Geforce GT 230M","nVidia Geforce GT 240M","nVidia Geforce GT 320M","nVidia Geforce GT 325M","nVidia Geforce GT 330","nVidia Geforce GT 330M","nVidia Geforce GT 335M","nVidia Geforce GT 415M","nVidia Geforce GT 420","nVidia Geforce GT 420M","nVidia Geforce GT 425M","nVidia Geforce GT 435M","nVidia Geforce GT 445M","nVidia Geforce GT 520M","nVidia Geforce GT 520MX","nVidia Geforce GT 525M","nVidia Geforce GT 540M","nVidia Geforce GT 545","nVidia Geforce GT 550M","nVidia Geforce GT 555M","nVidia Geforce GT 620M","nVidia Geforce GT 625M","nVidia Geforce GT 630M","nVidia Geforce GT 635","nVidia Geforce GT 635M","nVidia Geforce GT 640M","nVidia Geforce GT 640M LE","nVidia Geforce GT 645","nVidia Geforce GT 645M","nVidia Geforce GT 650M","nVidia Geforce GT 710M","nVidia Geforce GT 720A","nVidia Geforce GT 720M","nVidia Geforce GT 730A","nVidia Geforce GT 730M","nVidia Geforce GT 735M","nVidia Geforce GT 740M","nVidia Geforce GT 745A","nVidia Geforce GT 745M","nVidia Geforce GT 750M","nVidia Geforce GT 755M","nVidia Geforce GT 820M","nVidia Geforce GT625M","nVidia Geforce GTS 160M","nVidia Geforce GTS 250M","nVidia Geforce GTS 350M","nVidia Geforce GTS 360M","nVidia Geforce GTX 1050","nVidia Geforce GTX 1050 Ti","nVidia Geforce GTX 1060 with Max-Q Design","nVidia Geforce GTX 1070 with Max-Q Design","nVidia Geforce GTX 1080 with Max-Q Design","nVidia Geforce GTX 260M","nVidia Geforce GTX 280M","nVidia Geforce GTX 285M","nVidia Geforce GTX 460M","nVidia Geforce GTX 470M","nVidia Geforce GTX 480M","nVidia Geforce GTX 485M","nVidia Geforce GTX 560M","nVidia Geforce GTX 570M","nVidia Geforce GTX 580M","nVidia Geforce GTX 660M","nVidia Geforce GTX 670M","nVidia Geforce GTX 670MX","nVidia Geforce GTX 675M","nVidia Geforce GTX 675MX","nVidia Geforce GTX 680M","nVidia Geforce GTX 680MX","nVidia Geforce GTX 760A","nVidia Geforce GTX 760M","nVidia Geforce GTX 765M","nVidia Geforce GTX 770M","nVidia Geforce GTX 775M","nVidia Geforce GTX 780M","nVidia Geforce GTX 850A","nVidia Geforce GTX 850M","nVidia Geforce GTX 860M","nVidia Geforce GTX 870M","nVidia Geforce GTX 880M","nVidia Geforce GTX 950A","nVidia Geforce GTX 950M","nVidia Geforce GTX 960A","nVidia Geforce GTX 960M","nVidia Geforce GTX 965M","nVidia Geforce GTX 970M","nVidia Geforce GTX 980M","nVidia Geforce MX150","nVidia Geforce2 GTS/nVidia Geforce2 Pro","nVidia Geforce2 Integrated GPU","nVidia Geforce2 MX 100/200","nVidia Geforce2 MX/MX 400","nVidia Geforce3 Ti 200","nVidia Geforce3 Ti 500","nVidia Geforce4 420 Go","nVidia Geforce4 420 Go 32M","nVidia Geforce4 4200 Go","nVidia Geforce4 440 Go","nVidia Geforce4 440 Go 64M","nVidia Geforce4 448 Go","nVidia Geforce4 460 Go --MobileForce M4 Stock--","nVidia Geforce4 MX 4000","nVidia Geforce4 MX 420","nVidia Geforce4 MX 440","nVidia Geforce4 MX 440 with AGP8X","nVidia Geforce4 MX 440SE","nVidia Geforce4 MX 460","nVidia Geforce4 MX Integrated GPU","nVidia Geforce4 Ti 4200","nVidia Geforce4 Ti 4400","nVidia Geforce4 Ti 4600","nVidia Geforce4 Ti 4800 SE","nVidia Geforce9400M","GF117","GIGABYTE RADEON 9600 PRO","GRID M60-1Q","GRID M60-2Q","GRID M60-8Q","HD6450","Intel - Express Chipset G41","Intel - Express Chipset Q45/Q43","Intel 82845G Controller","Intel 82845G/GL Controller","Intel 82845G/GL/GE/PE/GV Controller","Intel 82865G Controller","Intel 82915G Express","Intel 82915G/GV/910GL Express","Intel 82945G Express","Intel 865 Embedded Controller","Intel 946GZ Embedded Chipset Function 0","Intel 946GZ Express","Intel B43 Express Chipset","Intel G35 Express","Intel G41 Express Chipset","Intel G41 Express Chipset v2","Intel G41 Express-Chipsatz","Intel G965 Express","Intel Haswell HD - GT1","Intel Haswell HD - GT2","Intel HD 3000","Intel HD Graphics 4000","Intel HD Graphics 4400","Intel HD Graphics 5000","Intel HD Graphics 510","Intel HD Graphics 515","Intel HD Graphics 520","Intel HD Graphics 5200","Intel HD Graphics 530","Intel HD Graphics 5300","Intel HD Graphics 5500","Intel HD Graphics 5600","Intel HD Graphics 6000","Intel HD Graphics 610","Intel HD Graphics 615","Intel HD Graphics 620","Intel HD 630","Intel HD Family","Intel HD Modded","Intel HD P3000","Intel HD P4000","Intel HD P4600","Intel HD P4600/P4700","Intel HD P530","Intel HD P630","Intel Iris 5100","Intel Iris 540","Intel Iris 550","Intel Iris 6100","Intel Iris Plus 640","Intel Iris Plus 650","Intel Iris Pro 5200","Intel Iris Pro 580","Intel Iris Pro 6200","Intel Iris Pro P580","Intel Media Accelerator 3150","Intel Media Accelerator 500","Intel Media Accelerator 600","Intel Media Accelerator HD","Intel Q33 Express","Intel Q35 Express","Intel Q45/Q43 Express Chipset","Intel Q45/Q43 Express-Chipsatz","Intel Q965/Q963 Express","Intel Skylake HD DT GT2","Intel UHD 620","Intel US15 Embedded Media and Controller","ION","ION LE","KB 2C","M860G with Mobility Radeon 4100","M880G with Mobility Radeon HD 4200","M880G with Mobility Radeon HD 4225","M880G with Mobility Radeon HD 4250","Matrox C680 PCIe x16","Matrox C900 PCIe x16","Matrox G200e WDDM 1.2","Matrox G200eh","Matrox G200eh WDDM 1.2","Matrox G200eR","Matrox G200eR WDDM 1.2","Matrox G200eW","Matrox G200eW WDDM 1.2","Matrox M9140 LP PCIe x16","Matrox Millennium P650 PCIe 128","Matrox Millennium P690 PCIe x16","Matrox Millennium P690 Plus LP PCIe x16","Matrox Parhelia APVe","MEDION RADEON X740XL","Mobile Intel - famiglia Express Chipset 45","Mobile Intel - famiglia Express Chipset serie 4","Mobile Intel 4 Express-Chipsatzfamilie","Mobile Intel 45 Express","Mobile Intel 45 Express-Chipsatzfamilie","Mobile Intel 915GM/GMS/910GML Express","Mobile Intel 945 Express","Mobile Intel 945GM Express","Mobile Intel 945GM/GU Express","Mobile Intel 965 Express","Mobile Intel 965 Express-Chipsatzfamilie","Mobile Intel HD","Mobile Intel serie 4 Express","Mobility Radeon 4100","MOBILITY RADEON 7000 IGP","MOBILITY RADEON 7500","MOBILITY RADEON 9000","MOBILITY RADEON 9000 IGP","MOBILITY RADEON 9000/9100 IGP","MOBILITY RADEON 9100 IGP","MOBILITY RADEON 9200","MOBILITY RADEON 9600 PRO TURBO","MOBILITY RADEON 9600/9700","MOBILITY RADEON 9700","MOBILITY RADEON 9800","Mobility Radeon HD 2300","Mobility Radeon HD 2400","Mobility Radeon HD 2400 XT","Mobility Radeon HD 2600","Mobility Radeon HD 2600 XT","Mobility Radeon HD 3410","Mobility Radeon HD 3430","Mobility Radeon HD 3450","Mobility Radeon HD 3470","Mobility Radeon HD 3470 Hybrid X2","Mobility Radeon HD 3650","Mobility Radeon HD 3670","Mobility Radeon HD 3850","Mobility Radeon HD 3870","Mobility Radeon HD 3870 X2","Mobility Radeon HD 4200","Mobility Radeon HD 4225","Mobility Radeon HD 4250","Mobility Radeon HD 4270","Mobility Radeon HD 4330","Mobility Radeon HD 4350","Mobility Radeon HD 4550","Mobility Radeon HD 4570","Mobility Radeon HD 4650","Mobility Radeon HD 4670","Mobility Radeon HD 4830","Mobility Radeon HD 4850","Mobility Radeon HD 4870","Mobility Radeon HD 5000","Mobility Radeon HD 5000 Serisi","Mobility Radeon HD 5165","Mobility Radeon HD 530v","Mobility Radeon HD 540v","Mobility Radeon HD 5430","Mobility Radeon HD 5450","Mobility Radeon HD 545v","Mobility Radeon HD 5470","Mobility Radeon HD 550v","Mobility Radeon HD 5570","Mobility Radeon HD 560v","Mobility Radeon HD 5650","Mobility Radeon HD 565v","Mobility Radeon HD 5730","Mobility Radeon HD 5850","Mobility Radeon HD 5870","Mobility Radeon HD serie 4200","Mobility Radeon X1300","Mobility Radeon X1350","Mobility Radeon X1400","Mobility Radeon X1450","Mobility Radeon X1600","Mobility Radeon X1700","MOBILITY RADEON X1800","Mobility Radeon X1900","Mobility Radeon X2300","Mobility Radeon X2300 HD","Mobility Radeon X2500","MOBILITY RADEON X300","MOBILITY RADEON X600","MOBILITY RADEON X600 SE","MOBILITY RADEON X700","MOBILITY RADEON XPRESS 200","Mobility Radeon. HD 5470","MOBILITY/RADEON 9000","MxGPU","nForce 750a SLI","nForce 760i SLI","nForce 780a SLI","nForce 980a/780a SLI","NVS 810","OpenXT Display Driver","PHDGD Ivy 4","PHDGD Quebec 4.0 for Intel Q45/Q43 Express Chipset","PHDGD Solo 1.2.0 x86","PHDGD Solo 2 x64","Quadro 1100M","Quadro 2000 D","Quadro 2000D","Quadro 280 NVS PCIe","Quadro CX","Quadro FX 4700 X2","Quadro FX 500/600 PCI","Quadro FX 500/FX 600","Quadro FX 5600","Quadro FX Go1400","Quadro GP100","Quadro K2200M","Quadro K620M","Quadro M1000M","Quadro M1200","Quadro M2000M","Quadro M2200","Quadro M3000M","Quadro M4000M","Quadro M5000M","Quadro M500M","Quadro M520","Quadro M5500","Quadro M600M","Quadro M620","Quadro NVS 210S","Quadro NVS 210S / nVidia Geforce 6150LE","Quadro NVS 280 SD","Quadro NVS 285","Quadro NVS 285 128MB","Quadro NVS 290","Quadro NVS 420","Quadro NVS 440","Quadro NVS 450","Quadro NVS 55/280 PCI","Quadro P1000","Quadro P3000","Quadro P400","Quadro P4000","Quadro P600","Quadro4 380 XGL","Quadro4 980 XGL","Radeon 2100","Radeon 3000","Radeon 3100","Radeon 540","Radeon 6600M","Radeon 6750M","RADEON 7000 / RADEON VE Family","RADEON 7500 Family","RADEON 9000 Family","RADEON 9100 Family","RADEON 9100 IGP","RADEON 9200 LE Family","RADEON 9200 PRO Family","RADEON 9500 PRO / 9700","Radeon 9550 / X1050","RADEON 9600 Family","RADEON 9600 PRO Family","RADEON 9600 TX Family","RADEON 9600SE","Radeon E","RADEON E4690","Radeon E6760","Radeon E8860","Radeon HD 2400","Radeon HD 2400 PCI","Radeon HD 2600 Pro AGP","Radeon HD 3200","Radeon HD 3300","Radeon HD 3650 AGP","Radeon HD 3670","Radeon HD 4270","Radeon HD 4300/4500 Serisi","Radeon HD 4330","Radeon HD 4650 AGP","Radeon HD 5470","Radeon HD 5600/5700","Radeon HD 6230","Radeon HD 6250","Radeon HD 6290","Radeon HD 6290M","Radeon HD 6300M","Radeon HD 6310","Radeon HD 6320","Radeon HD 6320 Graphic","Radeon HD 6320M","Radeon HD 6370M","Radeon HD 6380G","Radeon HD 6430M","Radeon HD 6450A","Radeon HD 6470M","Radeon HD 6480G","Radeon HD 6490M","Radeon HD 6520G","Radeon HD 6550A","Radeon HD 6610M","Radeon HD 6620G","Radeon HD 6630M","Radeon HD 6650M","Radeon HD 6670 + 6670 Dual","Radeon HD 6700M","Radeon HD 6750M","Radeon HD 6770M","Radeon HD 6800M","Radeon HD 6900M","Radeon HD 7290","Radeon HD 7310","Radeon HD 7310G","Radeon HD 7310M","Radeon HD 7340","Radeon HD 7340G","Radeon HD 7340M","Radeon HD 7400G","Radeon HD 7420G","Radeon HD 7450A","Radeon HD 7450M","Radeon HD 7470M","Radeon HD 7500G","Radeon HD 7500G + 7500M/7600M Dual","Radeon HD 7500G + 7550M Dual","Radeon HD 7500G + HD 7500M/7600M Dual","Radeon HD 7520G","Radeon HD 7520G + 7400M Dual","Radeon HD 7520G + 7600M Dual","Radeon HD 7520G + 7610M Dual","Radeon HD 7520G + 7650M Dual","Radeon HD 7520G + 7670M Dual","Radeon HD 7520G + 7700M Dual","Radeon HD 7520G + 8600/8700M Dual","Radeon HD 7520G + HD 7400M Dual","Radeon HD 7520G + HD 7600M Dual","Radeon HD 7520G + HD 7670M Dual","Radeon HD 7520G + HD 8600/8700M Dual","Radeon HD 7520G + HD 8750M Dual","Radeon HD 7540D + 6570 Dual","Radeon HD 7550M","Radeon HD 7550M/7650M","Radeon HD 7560D + 6570 Dual","Radeon HD 7560D + 6670 Dual","Radeon HD 7560D + 7560D Dual","Radeon HD 7560D + 7670 Dual","Radeon HD 7560D + HD 7000 Dual","Radeon HD 7560D + HD 7700 Dual","Radeon HD 7560D + R5 235 Dual","Radeon HD 7570M","Radeon HD 7570M/HD 7670M","Radeon HD 7580D","Radeon HD 7600G","Radeon HD 7600G + 7450M Dual","Radeon HD 7600G + 7500M/7600M Dual","Radeon HD 7600G + 7550M Dual","Radeon HD 7600G + 8500M/8700M Dual","Radeon HD 7600G + HD 7500M/7600M Dual","Radeon HD 7600G + HD 7550M Dual","Radeon HD 7600G + HD 8670M Dual","Radeon HD 7600G + HD Dual","Radeon HD 7600M + 7600M Dual","Radeon HD 7610M","Radeon HD 7620G","Radeon HD 7620G + 8600M Dual","Radeon HD 7620G + 8670M Dual","Radeon HD 7620G + HD 8600M Dual","Radeon HD 7620G + HD 8670M Dual","Radeon HD 7640G","Radeon HD 7640G + 6400M Dual","Radeon HD 7640G + 7400M Dual","Radeon HD 7640G + 7470M Dual","Radeon HD 7640G + 7500/7600 Dual","Radeon HD 7640G + 7600M Dual","Radeon HD 7640G + 7610M Dual","Radeon HD 7640G + 7670M Dual","Radeon HD 7640G + 7700M Dual","Radeon HD 7640G + 8500M Dual","Radeon HD 7640G + 8570M Dual","Radeon HD 7640G + 8600/8700M Dual","Radeon HD 7640G + 8670M Dual","Radeon HD 7640G + 8750M Dual","Radeon HD 7640G + HD 7400M Dual","Radeon HD 7640G + HD 7600M Dual","Radeon HD 7640G + HD 7670M Dual","Radeon HD 7640G + HD 7700M Dual","Radeon HD 7640G + HD 8500M Dual","Radeon HD 7640G + HD 8500M N HD 8500M Dual","Radeon HD 7640G + HD 8570M Dual","Radeon HD 7640G + HD 8600/8700M Dual","Radeon HD 7640G + HD 8750M Dual","Radeon HD 7640G + R5 M200 Dual","Radeon HD 7640G N HD 7640G + HD 7600M N HD 7600M D","Radeon HD 7640G N HD 7640G + HD 7670M Dual","Radeon HD 7650A","Radeon HD 7650M","Radeon HD 7660D + 6570 Dual","Radeon HD 7660D + 6670 Dual","Radeon HD 7660D + 7470 Dual","Radeon HD 7660D + 7670 Dual","Radeon HD 7660D + HD 6670 Dual","Radeon HD 7660D + HD 7000 Dual","Radeon HD 7660D + HD 7700 Dual","Radeon HD 7660D + R7 240 Dual","Radeon HD 7660G","Radeon HD 7660G + 7400M Dual","Radeon HD 7660G + 7470M Dual","Radeon HD 7660G + 7600M Dual","Radeon HD 7660G + 7610M Dual","Radeon HD 7660G + 7670M Dual","Radeon HD 7660G + 7700M Dual","Radeon HD 7660G + 7730M Dual","Radeon HD 7660G + 8600M Dual","Radeon HD 7660G + 8670M Dual","Radeon HD 7660G + HD 7500M/7600M Dual","Radeon HD 7660G + HD 7600M Dual","Radeon HD 7660G + HD 7670M Dual","Radeon HD 7660G + HD 7700M Dual","Radeon HD 7660G + HD 7730M Dual","Radeon HD 7660G + HD 8670M Dual","Radeon HD 7660G N HD 7660G + HD 7600M N HD 7600M D","Radeon HD 7660G N HD 7660G + HD 7670M Dual","Radeon HD 7660G N HD 7660G + HD 7700M N HD 7700M D","Radeon HD 7670A","Radeon HD 7670M","Radeon HD 7670M + 7670M Dual","Radeon HD 7690M","Radeon HD 7690M XT","Radeon HD 7730M","Radeon HD 7750M","Radeon HD 7850M","Radeon HD 7870M","Radeon HD 7970M","Radeon HD 8180","Radeon HD 8210","Radeon HD 8240","Radeon HD 8250","Radeon HD 8280","Radeon HD 8280E","Radeon HD 8280G","Radeon HD 8330","Radeon HD 8330E","Radeon HD 8350G","Radeon HD 8370D","Radeon HD 8400","Radeon HD 8400E","Radeon HD 8410G","Radeon HD 8450G","Radeon HD 8450G + 8600M Dual","Radeon HD 8450G + 8670M Dual","Radeon HD 8450G + 8750M Dual","Radeon HD 8450G + HD 8600M Dual","Radeon HD 8450G + HD 8750M Dual","Radeon HD 8470D","Radeon HD 8470D + 6450 Dual","Radeon HD 8500M","Radeon HD 8500M/8700M","Radeon HD 8510G","Radeon HD 8510G + 8500M Dual","Radeon HD 8550D","Radeon HD 8550G","Radeon HD 8550G + 8500M Dual","Radeon HD 8550G + 8570M Dual","Radeon HD 8550G + 8600/8700M Dual","Radeon HD 8550G + 8600M Dual","Radeon HD 8550G + 8670M Dual","Radeon HD 8550G + 8690M Dual","Radeon HD 8550G + 8750M Dual","Radeon HD 8550G + HD 7600M Dual","Radeon HD 8550G + HD 8570M Dual","Radeon HD 8550G + HD 8600/8700M Dual","Radeon HD 8550G + HD 8600M Dual","Radeon HD 8550G + HD 8670M Dual","Radeon HD 8550G + HD 8750M Dual","Radeon HD 8550G + R5 M200 Dual","Radeon HD 8550G + R5 M230 Dual","Radeon HD 8570 + 8670D Dual","Radeon HD 8570D","Radeon HD 8570D + 6570 Dual","Radeon HD 8570D + HD 6570 Dual","Radeon HD 8570D + HD 6670 Dual","Radeon HD 8570D + HD 7000 Dual","Radeon HD 8570D + HD 7700 Dual","Radeon HD 8570D + HD 8570 Dual","Radeon HD 8570D + R7 200 Dual","Radeon HD 8570D + R7 240 Dual","Radeon HD 8570M","Radeon HD 8600/8700M","Radeon HD 8610G","Radeon HD 8610G + 8500M Dual","Radeon HD 8610G + 8600M Dual","Radeon HD 8610G + 8670M Dual","Radeon HD 8610G + HD 8500M Dual","Radeon HD 8610G + HD 8600M Dual","Radeon HD 8610G + HD 8670M Dual","Radeon HD 8610G + R5 M200 Dual","Radeon HD 8650D","Radeon HD 8650G","Radeon HD 8650G + 7600M Dual","Radeon HD 8650G + 7670M Dual","Radeon HD 8650G + 8500M Dual","Radeon HD 8650G + 8570M Dual","Radeon HD 8650G + 8600/8700M Dual","Radeon HD 8650G + 8600M Dual","Radeon HD 8650G + 8670M Dual","Radeon HD 8650G + 8750M Dual","Radeon HD 8650G + HD 7600M Dual","Radeon HD 8650G + HD 7670M Dual","Radeon HD 8650G + HD 8570M Dual","Radeon HD 8650G + HD 8600/8700M Dual","Radeon HD 8650G + HD 8600M Dual","Radeon HD 8650G + HD 8670M Dual","Radeon HD 8650G + HD 8750M Dual","Radeon HD 8650G + R5 M200 Dual","Radeon HD 8650G + R5 M230 Dual","Radeon HD 8650G N HD 8650G + HD 8570M Dual","Radeon HD 8650G N HD 8650G + HD 8600M N HD 8600M D","Radeon HD 8670D","Radeon HD 8670D + 6670 Dual","Radeon HD 8670D + 7700 Dual","Radeon HD 8670D + HD 6670 Dual","Radeon HD 8670D + HD 7000 Dual","Radeon HD 8670D + R5 235 Dual","Radeon HD 8670D + R7 200 Dual","Radeon HD 8670D + R7 240 Dual","Radeon HD 8670M","Radeon HD 8690A","Radeon HD 8690M","Radeon HD 8730M","Radeon HD 8750M","Radeon HD 8790M","Radeon HD 8790M / R9 M290X","Radeon HD 8850M","Radeon HD 8850M / R9 M265X","Radeon HD 8870M","Radeon HD 8870M / R9 M270X / M370X","Radeon HD 8970M","RADEON HD6370D","RADEON HD6410D","RADEON HD6530D","Radeon HD7570","Radeon HD8490","Radeon HD8970M","Radeon IGP 320M","Radeon IGP 340M","RADEON IGP 345M","RADEON IGP 350M","Radeon Pro WX 2100","Radeon Pro WX 3100","Radeon Pro WX 4100","Radeon Pro WX 5100","Radeon Pro WX 7100","Radeon Pro WX4100","Radeon R2","Radeon R2E","Radeon R3","Radeon R3E","Radeon R4","Radeon R5 235 + HD 7560D Dual","Radeon R5 310","Radeon R5 430","Radeon R5 A10-9600P RADEON R5, 10 COMPUTE CORES 4C","Radeon R5 A10-9630P RADEON R5, 10 COMPUTE CORES 4C","Radeon R5 M230","Radeon R5 M240","Radeon R5 M255","Radeon R5 M315","Radeon R5 M320","Radeon R5 M330","Radeon R5 M335","Radeon R5 M430","Radeon R5 Opteron X3216","Radeon R5 PRO A10-8730B R5, 10 COMPUTE CORES 4C+6G","Radeon R5 PRO A6-8570 R5, 8 COMPUTE CORES 2C+6G","Radeon R5 PRO A6-9500E R5, 6 COMPUTE CORES 2C+4G","Radeon R5 PRO A8-9600B R5, 10 COMPUTE CORES 4C+6G","Radeon R5E","Radeon R6","Radeon R6 + R7 M265DX Dual","Radeon R6 A10-8700P","Radeon R6 A8-8600P","Radeon R6 PRO A10-8700B R6, 10 Compute Cores 4C+6G","Radeon R6 PRO A8-8600B R6, 10 Compute Cores 4C+6G","Radeon R7 + HD 7700 Dual","Radeon R7 + R5 330 Dual","Radeon R7 + R5 435 Dual A10-9700 RADEON","Radeon R7 + R7 200 Dual","Radeon R7 + R7 240 Dual","Radeon R7 + R7 350 Dual","Radeon R7 240 + HD 8570D Dual","Radeon R7 240 + HD 8670D Dual","Radeon R7 340","Radeon R7 370","Radeon R7 430","Radeon R7 A10 Extreme Edition","Radeon R7 A10 PRO-7800B","Radeon R7 A10 PRO-7850B","Radeon R7 A10-7700K","Radeon R7 A10-7800","Radeon R7 A10-7860K","Radeon R7 A10-7870K","Radeon R7 A10-7890K","Radeon R7 A10-8750","Radeon R7 A10-9700 RADEON","Radeon R7 A12-9700P RADEON","Radeon R7 A12-9720P RADEON","Radeon R7 A12-9800 RADEON","Radeon R7 A12-9800E RADEON","Radeon R7 A265","Radeon R7 A370","Radeon R7 A8 PRO-7600B","Radeon R7 A8-7600","Radeon R7 A8-7650K","Radeon R7 A8-7670K","Radeon R7 A8-8650","Radeon R7 A8-9600 RADEON","Radeon R7 FX-8800P","Radeon R7 FX-9800P RADEON","Radeon R7 FX-9830P RADEON","Radeon R7 M260","Radeon R7 M260X","Radeon R7 M265","Radeon R7 M270","Radeon R7 M340","Radeon R7 M350","Radeon R7 M360","Radeon R7 M365X","Radeon R7 M370","Radeon R7 M440","Radeon R7 M445","Radeon R7 M460","Radeon R7 M465","Radeon R7 PRO A10-8750B","Radeon R7 PRO A10-8770","Radeon R7 PRO A10-8770E","Radeon R7 PRO A10-8850B","Radeon R7 PRO A10-9700","Radeon R7 PRO A10-9700E","Radeon R7 PRO A12-8800B","Radeon R7 PRO A12-8830B","Radeon R7 PRO A12-8870","Radeon R7 PRO A12-8870E","Radeon R7 PRO A12-9800","Radeon R7 PRO A12-9800B","Radeon R7 PRO A12-9800E","Radeon R7 PRO A8-8650B","Radeon R7 PRO A8-8670E","Radeon R7 PRO A8-9600","Radeon R9 260","Radeon R9 M265X","Radeon R9 M270X","Radeon R9 M275","Radeon R9 M275X / M375","Radeon R9 M290X","Radeon R9 M295X","Radeon R9 M360","Radeon R9 M370X","Radeon R9 M375","Radeon R9 M375X","Radeon R9 M380","Radeon R9 M390X","Radeon R9 M395","Radeon R9 M395X","Radeon R9 M470X","Radeon RX Vega","Radeon TM R9 A360","Radeon X1200","Radeon X1250","Radeon X1270","Radeon X1300 PRO","Radeon X1550 64-bit","Radeon X1600","Radeon X1600 Pro / X1300XT","Radeon X1650 GTO","Radeon X1650 SE","Radeon X1700 Targa Edition","RADEON X300SE","RADEON X550XT","Radeon X550XTX","RADEON X600XT","RADEON X800GT","Radeon Xpress 1100","Radeon Xpress 1150","Radeon Xpress 1200","Radeon Xpress 1250","Radeon Xpress 1270","RADEON XPRESS 200","RADEON XPRESS 200M","RadeonT R7 450","Rage Fury Pro/Xpert 2000 Pro","RIVA TNT2 Model 64/Model 64 Pro","RIVA TNT2/TNT2 Pro","RV530 PRO","S3 Chrome 430 ULP","S3 ProSavageDDR","SAPPHIRE RADEON 9600 ATLANTIS","SAPPHIRE Radeon X1550","Sapphire RADEON X800 GT","Sherry 1.3 for GMA 3150","Sherry 1.3.2 beta for 945 chipsets","SiS 630/730","SiS 650_651_M650_M652_740","SiS 651","SiS 661FX","SiS 661FX/GX Mirage","SiS 661FX_760_741_M661FX_M760_M741","SiS 741","SiS 760","SiS M661MX","SiS M760GX","SiS Mirage","SiS Mirage 3","SUMO 9640","SUMO 964A","Tesla C2050","Tesla C2075","TRINITY DEVASTATOR MOBILE","Vanta/Vanta LT","VIA Chrome9 HC IGP","VIA Chrome9 HC IGP Family","VIA Chrome9 HC IGP Family WDDM","VIA Chrome9 HC IGP Prerelease WDDM 1.1","VIA Chrome9 HC IGP WDDM","VIA Chrome9 HC IGP WDDM 1.1","VIA Chrome9 HD IGP","VIA/S3G Chrome 645/640 GPU","VIA/S3G DeltaChrome IGP","VIA/S3G KM400/KN400","VIA/S3G UniChrome IGP","VIA/S3G UniChrome Pro IGP","VIA/S3G UniChromeII","VirtualBox Adapter for Windows 8+","Wine Display Adapter"];
 $scope.laptop_lecteurs = [
                            'Aucun Lecteur',
                            'D-ROM',
                            'CD-RW/DVD-ROM',
                            'DVD-ROM',
                            'Graveur Blu-ray',
                            'Graveur DVD',
                            'Lecteur Blur-ray/DVD+-RW Combo'];

 $scope.laptop_proprietes_values = [
   "Ecran IGZO", "Ecran IP", "Ecran OLED", "Ecran TFT", "Ecran anti-reflets (mat)", "Ecran brillant",
   "Ecran large", "Ecran multi-touch", "Ecran tactile", "Ecran à rétroéclairage LED", "Ecran amovible",
   "Ecran anti-rayures", "Ecran anti-reflets", "Ecran anti-traces de doigts", "Ecran capacitif",
   "Ecran convertible", "Ecran mat", "Ecran tactile multi-touch 10 points",
   "Ecran tactile multi-touch 5 points"
 ]

  $scope.laptop_proprietes = {
    values: []
  }

  $scope.laptop_proprietes_checkAll = function() {
    $scope.laptop_proprietes.values = angular.copy($scope.laptop_proprietes_values);
  };
  $scope.laptop_proprietes_uncheckAll = function() {
    $scope.laptop_proprietes.values = [];
  };


 $scope.laptop_proprietes_model2 = [];
 $scope.laptop_proprietes_settings = { scrollableHeight: '100px', scrollable: true };
 // $scope.laptop_proprietes_customTexts = {buttonDefaultText: 'Sélectionner'};
 
  $scope.sortie_video_values = [
    "DisplayPort", "HDMI", "HDMI 2.0", "Intel Thunderbolt", "Micro-HDMI", "Mini-DisplayPort",
    "Mini-HDMI", "S-Video", "Thunderbolt 2", "Thunderbolt 3", "VGA D-Sub (HD-15)"
  ]

  $scope.laptop_sortie_video = {
    values: []
  }

  $scope.laptop_sortie_video_checkAll = function() {
    $scope.laptop_sortie_video.values = angular.copy($scope.sortie_video_values);
  };
  $scope.laptop_sortie_video_uncheckAll = function() {
    $scope.laptop_sortie_video.values = [];
  };

 $scope.laptop_sortie_video_model2 = [];
 //$scope.laptop_sortie_video_settings = { checkboxes: true, };
 
 // $scope.laptop_sortie_video_customTexts = {buttonDefaultText: 'Sélectionner'};

 // ====================================  LAVE-LINGE LISTS ==============================================//

 $scope.type_lavelinge =  [];
 $scope.type_charge_lavelinge =[];
 $scope.Couleur_Lavelinge = [];

 // ====================================  SECHE-LINGE LISTS ==============================================//
 // ====================================  MODELES LISTS ==============================================//
 
  
  // ====================================  DAMAGES LISTS ==============================================//

  $scope.typeBien_damage = [];

  $scope.seche_linge_damage =
  [{"name":"Dommage Electrique"}, 
  {"name":"Autre"}];

  $scope.telephone_damage = 
  [{"name":"Dommage Electrique"}, 
  {"name":"Autre"}];

  $scope.lave_linge_damage = 
  [{"name":"Dommage Electrique"},
  {"name":"Origine mécanique (filtre)"},
  {"name":"Origine mécanique (module)"},
  {"name":"Origine mécanique (valvule électronique)"},
  {"name":"Origine mécanique (Programateur)"},
  {"name":"Origine mécanique (résistance moteur) "}];

  $scope.tv_damage = 
  [{"name":"Dommage Electrique"},
  {"name":"Dalle"},
  {"name":"Autre"}];

  $scope.Lave_vaisselle_damage = 
  [{"name":"Dommage Electrique"},
  {"name":"Origine mécanique (filtre)"},
  {"name":"Origine mécanique (résistance)"},
  {"name":"Origine mécanique (stop-eau)"},
  {"name":"Origine mécanique (Programateur détergent)"},
  {"name":"Origine mécanique (pompe)"}];

  $scope.refrigerateurs_damage =
  [{"name":"Dommage Electrique"},
  {"name":"Origine mécanique (compresseur)"},
  {"name":"Origine mécanique (Thermostat)"},
  {"name":"Origine mécanique (Timer)"}];

  $scope.reparation_values = [
    'Ecran', 'Chassis tordu', "Oxydation/prise d'eau", 'Ne sÕallume plus', 'CamŽra avant',
    'CamŽra arrire', 'Lecteur SIM', 'Lecteur SD', 'Batterie', 'Ecouteur', 'Haut parleur Žcoute',
    'Micro', 'Vibreur', 'Bouton vibreur', 'Wifi', 'Boutons volume', 'GSM', 'Bluetooth',
    'Autre', 'Lecteur SIM & SD', 'Problme de charge', 'Bouton Power', 'Flash'
  ]

  $scope.reparation = {
    values: []
  }

  $scope.reparation_checkAll = function() {
    $scope.reparation.values = angular.copy($scope.reparation_values);
  };
  $scope.reparation_uncheckAll = function() {
    $scope.reparation.values = [];
  };

  // $scope.links_aiude = {
  //   'Réfrigérateurs': "https://zingtree.com/host.php?style=buttons&tree_id=697555473&persist_names=Restart&persist_node_ids=1", 
  //   'Téléviseurs': "https://zingtree.com/host.php?style=buttons&tree_id=340156992&persist_names=Restart&persist_node_ids=1",
  //   //'Laptops': "https://zingtree.com/host.php?style=buttons&tree_id=340156992&persist_names=Restart&persist_node_ids=1",
  //   //'Téléphonie mobile': "https://zingtree.com/host.php?style=buttons&tree_id=340156992&persist_names=Restart&persist_node_ids=1"
  // };
  
  

});

