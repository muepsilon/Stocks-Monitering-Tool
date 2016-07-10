// List all directives

(function(){

  angular.module("stockWatch.directives")
  .directive('hideDropdowns', function($document){

    return {
      restrict: 'E',
      scope: {
        isvisible: '='
      },
      link: function(scope, element, attr){
        
          scope.isvisible = false;

          scope.toggleSelect = function(){
            scope.isvisible = !scope.isvisible;
          } 
          $document.bind('click', function(event){
            var isClickedElementChildOfPopup = element
              .find(event.target)
              .length > 0;
            if (isClickedElementChildOfPopup)
              return;
              
            scope.isvisible = false;
            scope.$apply();
          });
      }
    }
  });

  angular.module("stockWatch.directives")
  .directive('header',function(){
    return {
      restrict: 'E',
      scope: {},
      controller: ['$scope','Layout','$state',function($scope,Layout,$state){

        $scope.is_logged_in = false;
        $scope.check_session = check_session;

        Layout.is_logged_in()
        .then(function successCallback(response){
          $scope.is_logged_in = response.data.login;
        },function failureCallback(){
          
        });

        function check_session(){
          return $scope.is_logged_in;
        }
        $scope.login = function(){
          if ($state.current.name == 'company') {
            $state.go('accounts',{'redirect_state':$state.current.name,'endpoint':$state.params.name});
          } else {
            $state.go('accounts',{'redirect_state':$state.current.name});
          }
        }
        $scope.logout = function(){
          Layout.logout()
          .then(function successCallback(){
            $scope.is_logged_in = false;
            $state.go($state.current, {}, {reload: true});
          },function failureCallback(){

          });
        }
      }],
      templateUrl: '/static/partials/header.html'
    }
  });

  angular.module("stockWatch.directives")
  .directive('stockHistory',function(){
    return {
      restrict: 'E',
      scope: {},
      controller: ['$scope','Layout','$location','$filter','$state', function($scope,Layout,$location,$filter,$state){

        $scope.companySymbol = '';
        $scope.loadingData = false;
        $scope.dropdown = false;
        $scope.company_query = "";
        $scope.companySuggestion = [];
        $scope.timeframe = ['1m','3m','6m','1y','2y','5y','10y'];
        $scope.selectedTimeframe = 3;
        $scope.chart_options = {showXLabels: 10};
        $scope.labels = [];
        $scope.data = [[]];

        $scope.companyName = $location.path().split('/')[$location.path().split('/').length - 1].replace(/[-]/g,' ');
        
        Layout.validate_company_name($scope.companyName)
        .then(function successCallback(response){
          
          if (response.data.length != 0) {
            $scope.companySymbol = response.data[0].symbol;
            get_company_data($scope.companySymbol);
          }
        },function failureCallback(response){
        });
        
        function get_company_data(symbol,timeframe){

          timeframe = timeframe || $scope.timeframe[$scope.selectedTimeframe];

          var d;

          Layout.get_company_data(symbol,timeframe)
          .then(function successCallback(response){
               
            $scope.series = [response.data.dataset.dataset_code];
            $scope.labels = [];
            $scope.data = [[]];
            response.data.dataset.data.forEach(function(item){
              d = new Date(item[0]);
              if(timeframe[timeframe.length - 1] == 'm'){
                $scope.labels.push($filter('date')(d,'dd-MMM'));
              } else {
                $scope.labels.push($filter('date')(d, 'MMM-yy'));
              }
              $scope.data[0].push(item[5]);
            });
            $scope.loadingData = false;
          },function failureCallback(response){
            
          });
        }
        $scope.changeTimeframe = function(index){
              $scope.selectedTimeframe = index;
              $scope.loadingData = true;
              get_company_data($scope.companySymbol,$scope.timeframe[$scope.selectedTimeframe]);
        }
        $scope.searchSuggestion = function (){
          if ($scope.company_query != undefined && $scope.company_query.length > 0) {
            Layout.validate_company_name($scope.company_query)
            .then(function(response){
                $scope.companySuggestion = response.data;
                $scope.dropdown = true;
            });
          } else {
            $scope.companySuggestion = [];
            $scope.company_query = "";
          }
        }
        $scope.showSearchSuggestion = function () {
          $scope.company_query = $scope.company_query || "";
          return ($scope.companySuggestion.length > 0) &&  $scope.dropdown && $scope.company_query.length > 0 ;
        }
        $scope.selectCompany = function (item){
          var companyName = item.name;
          $state.go('company',{name: companyName.replace(/[ ]/g,'-')});
        }
      }],
      templateUrl: '/static/partials/chart.html'
    }
  });

})();