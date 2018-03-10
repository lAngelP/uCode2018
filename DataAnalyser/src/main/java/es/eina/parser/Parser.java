package es.eina.parser;

import es.eina.Main;
import es.eina.analysis.sentiment.SentimentAnalysis;
import es.eina.loader.Loader;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONWriter;

import java.io.*;
import java.net.*;

public class Parser {
    //private static final String key = "AIzaSyCdmrrnqlbT429pm_hi7LYIgmnyV_VS-YQ";
    private static final String key = "AIzaSyCyQ9rdMWrrTDMzXI8_XD3i_-57qU4-bNg";


    public static void parseFiles(File dir, File output, SentimentAnalysis analysis){
        output.mkdirs();
        File[] files = dir.listFiles();
        for (File s : files){
            File out = new File(output, s.getName());
            JSONArray object = Loader.loadData(s);
            JSONObject finalData = new JSONObject();
            JSONArray outArray = new JSONArray();

            for(int i = 0; i < object.length(); i++){
                System.out.println("Parsing " + ((double)i / object.length()));
                JSONObject result = new JSONObject();
                JSONObject user = new JSONObject();

                JSONObject obj = object.getJSONObject(i);
                JSONObject entities = obj.getJSONObject("entities");
                JSONArray hashtags = loadValue(entities.getJSONArray("hashtags"), "text");
                JSONArray mentions = loadValue(entities.getJSONArray("user_mentions"), "name");
                JSONArray urls = loadValue(entities.getJSONArray("urls"), "expanded_url");
                JSONObject userData = obj.getJSONObject("user");

                user.put("id", userData.getInt("id"));
                user.put("nick", userData.getString("name"));
                user.put("name", userData.getString("screen_name"));
                user.put("location", performHTTP(userData.getString("location")));
                user.put("description", userData.getString("description"));
                user.put("followers", userData.getInt("followers_count"));
                user.put("friends", userData.getInt("friends_count"));
                user.put("created_at", userData.getString("created_at"));
                user.put("profile_img", userData.getString("profile_image_url_https"));


                result.put("id", obj.getInt("id"));
                result.put("text", obj.getString("text"));
                result.put("hashtags", hashtags);
                result.put("mentions", mentions);
                result.put("urls", urls);
                result.put("user", user);
                result.put("sentient", analysis.analyse(obj.getString("text")));

                outArray.put(result);
            }

            finalData.put("team", s.getName());
            finalData.put("data", outArray);

            FileWriter writer = null;
            try {
                out.createNewFile();
                writer = new FileWriter(out);
                writer.append(finalData.toString());

            } catch (IOException e) {
                e.printStackTrace();
            }finally {
                try {
                    if (writer != null) {
                        writer.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private static JSONObject performHTTP(String location) {
        if(location == null || location.isEmpty()) return new JSONObject();

        URL url;
        try {
            url = new URL("https://maps.googleapis.com/maps/api/geocode/json?address="+URLEncoder.encode(location, "UTF-8")+"&key=" + key);
        } catch (MalformedURLException | UnsupportedEncodingException e) {
            e.printStackTrace();
            return new JSONObject();
        }
        HttpURLConnection con;
        try {
            con = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            e.printStackTrace();
            return new JSONObject();
        }
        try {
            con.setRequestMethod("GET");
        } catch (ProtocolException e) {
            e.printStackTrace();
            return new JSONObject();
        }

        BufferedReader in = null;
        try {
            in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuilder content = new StringBuilder();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }

            return parseJSON(content.toString());
        }catch(Exception ex){
            ex.printStackTrace();
        }finally{
            try {
                if (in != null) {
                    in.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return new JSONObject();
    }

    private static String getIndex(JSONArray address, int index){
        return address.getJSONObject(index).getString("long_name");
    }

    private static JSONObject parseJSON(String s) {
        JSONObject object = new JSONObject(s);
        JSONObject result = new JSONObject();


        JSONObject searchResult = object.getJSONArray("results").getJSONObject(0);
        JSONObject latlong = searchResult.getJSONObject("geometry").getJSONObject("bounds").getJSONObject("northeast");
        JSONArray address = searchResult.getJSONArray("address_components");

        result.put("lat", latlong.getDouble("lat"));
        result.put("long", latlong.getDouble("lng"));
        //result.put("location", getIndex(address,0) + "," + getIndex(address,1) + "," + getIndex(address,3) + "," + getIndex(address,4) + "," + getIndex(address,5) + "," + getIndex(address,6) + "," + getIndex(address,7));

        return result;
    }

    private static JSONArray loadValue(JSONArray base, String obtain){
        JSONArray array = new JSONArray();

        for(int i = 0; i < base.length(); i++){
            array.put(((JSONObject)base.get(i)).getString(obtain));
        }

        return array;
    }

}
