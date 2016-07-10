// Angular services

(function(){

  angular.module('stockWatch.services',[])
    .factory('Layout',Layout);

    Layout.$inject = ['$http'];

    function Layout($http){

      var BASE_URL = "http://market.com:8000/";

      var Layout = {
        get_stocks :      get_stocks,
        get_indices:      get_indices,
        get_stocks_watch: get_stocks_watch,
        delete_stock:     delete_stock,
        delete_stock_watch_list: delete_stock_watch_list,
        validate_company_name:  validate_company_name,
        get_company_data : get_company_data,
        add_stock:        add_stock,
        add_watch_stock:  add_watch_stock,
        is_logged_in:     is_logged_in,
        edit_stock:       edit_stock,
        edit_stock_watch_list: edit_stock_watch_list,
        login:            login,
        signup:           signup,
        logout:           logout,
        duplicateCheck:   duplicateCheck
      };

      return Layout;

      function get_stocks(){
        return $http.get(BASE_URL + "api/latestprice/stocks");
      }
      function get_indices () {
        return $http.get(BASE_URL + "api/latestprice/indices/");
      }
      function get_stocks_watch(){
        return $http.get(BASE_URL + "api/latestprice/watchstocks");
      }
      function delete_stock(id){
        return $http.delete(BASE_URL + "api/stocks/" + id.toString());
      }
      function delete_stock_watch_list(id){
        return $http.delete(BASE_URL + "api/watchstocks/" + id.toString());
      }
      function validate_company_name(query){
        return $http.get(BASE_URL + "api/company/find/?query=" + query)
        .success(function(){
        });
      }

      function add_stock(data){
        return $http.post(BASE_URL + "api/stocks/",data);
      }
      function add_watch_stock(data){
        return $http.post(BASE_URL + "api/watchstocks/",data);
      }
      function edit_stock(id, data){
        return $http.put(BASE_URL + "api/stocks/" + id.toString(), data);
      }
      function edit_stock_watch_list(id, data){
        return $http.put(BASE_URL + "api/watchstocks/" + id.toString(), data);
      }
      function login (data) {
        return $http.post(BASE_URL + "api/accounts/login/", data)
      }
      function signup (data) {
        return $http.post(BASE_URL + "api/accounts/signup/", data)
      }
      function logout () {
        return $http.post(BASE_URL + "api/accounts/logout/")
      }
      function duplicateCheck(credential){
        var query = "";
        credential = credential || {};
        credential.username = credential.username || "";
        credential.email = credential.email || "";
        query = "username="+credential.username+"&email="+credential.email;
        
        return $http.get(BASE_URL + "api/accounts/duplicatecheck/?"+query)
      }
      function is_logged_in(){
        return $http.post(BASE_URL + "api/accounts/verifysession/")
      }
      function get_company_data(symbol,timeframe){
        timeframe = timeframe || '1y'
        return $http.get(BASE_URL + "api/company/" + symbol + "?timeframe=" + timeframe)
      }
    };

})();