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

})();