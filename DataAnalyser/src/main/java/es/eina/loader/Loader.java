package es.eina.loader;

import org.json.JSONArray;
import org.json.JSONTokener;
import org.json.JSONObject;
import org.json.JSONWriter;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class Loader {

    public static JSONArray loadData(File f){
        try {
            return new JSONArray(readFile(f));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private static String readFile(File f) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(f));

        StringBuilder body = new StringBuilder();
        String line;

        while((line = reader.readLine()) != null){
            body.append(line);
        }

        return body.toString();
    }

}
