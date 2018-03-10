package es.eina.parser;

import es.eina.Main;
import es.eina.loader.Loader;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONWriter;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Parser {

    public static void parseFiles(File dir, File output){
        output.mkdirs();
        File[] files = dir.listFiles();
        for (File s : files){
            File out = new File(output, s.getName());
            JSONArray object = Loader.loadData(s);
            JSONObject finalData = new JSONObject();
            JSONArray outArray = new JSONArray();

            for(int i = 0; i < object.length(); i++){
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
                //user.put("location", TODO !!!)
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

    private static JSONArray loadValue(JSONArray base, String obtain){
        JSONArray array = new JSONArray();

        for(int i = 0; i < base.length(); i++){
            array.put(((JSONObject)base.get(i)).getString(obtain));
        }

        return array;
    }

}
