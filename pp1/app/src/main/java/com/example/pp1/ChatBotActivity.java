package com.example.pp1;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.button.MaterialButton;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class ChatBotActivity extends AppCompatActivity {

    private EditText chatInput;
    private LinearLayout chatContainer;
    private ScrollView chatScrollView;

    private final String apiKey = "AIzaSyCrrSm__EKxXf4qLmrRBuWrt5wV-HiwyDQ";
    private final String apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat_bot);

        chatInput = findViewById(R.id.chatInput);
        chatContainer = findViewById(R.id.chatContainer);
        chatScrollView = findViewById(R.id.chatScrollView);
        MaterialButton sendButton = findViewById(R.id.sendButton);

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String userInput = chatInput.getText().toString();
                if (!userInput.isEmpty()) {
                    addChatMessage("You: " + userInput, true);
                    chatInput.setText("");
                    fetchChatResponse(userInput);
                }
            }
        });
    }

    private void addChatMessage(final String message, final boolean isUser) {
        runOnUiThread(() -> {
            TextView messageTextView = new TextView(ChatBotActivity.this);
            messageTextView.setText(message);
            messageTextView.setTextSize(16);
            messageTextView.setPadding(10, 10, 10, 10);
            messageTextView.setTextColor(isUser ? getResources().getColor(R.color.black) : getResources().getColor(R.color.teal_700));
            chatContainer.addView(messageTextView);
            chatScrollView.post(() -> chatScrollView.fullScroll(View.FOCUS_DOWN));
        });
    }

    private void fetchChatResponse(final String question) {
        new Thread(() -> {
            try {
                URL url = new URL(apiUrl + "?key=" + apiKey);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setDoOutput(true);

                String jsonInputString = "{ \"contents\": [{ \"parts\": [{ \"text\": \"" + question + "\" }]}]}";

                OutputStream os = connection.getOutputStream();
                os.write(jsonInputString.getBytes());
                os.flush();
                os.close();

                BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                StringBuilder response = new StringBuilder();
                String output;
                while ((output = br.readLine()) != null) {
                    response.append(output);
                }
                connection.disconnect();
                parseResponse(response.toString());
            } catch (Exception e) {
                e.printStackTrace();
                addChatMessage("Error: " + e.getMessage(), false);
            }
        }).start();
    }

    private void parseResponse(final String jsonResponse) {
        try {
            JSONObject responseJson = new JSONObject(jsonResponse);
            JSONArray candidates = responseJson.getJSONArray("candidates");
            JSONObject content = candidates.getJSONObject(0).getJSONObject("content");
            JSONArray parts = content.getJSONArray("parts");
            String responseText = parts.getJSONObject(0).getString("text");

            addChatMessage("Bot: " + responseText, false);
        } catch (JSONException e) {
            e.printStackTrace();
            addChatMessage("Error parsing response: " + e.getMessage(), false);
        }
    }
}
