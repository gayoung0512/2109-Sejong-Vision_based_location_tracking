package com.cookandroid.albl_project;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
//import android.support.v7.app.ActionCompatActivity;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity{

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btnfood = (Button) findViewById(R.id.Food);
        btnfood.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), food.class);
                startActivity(intent);
            }
        });
        Button btnfashion = (Button) findViewById(R.id.Fashion);
        btnfashion.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), fashion.class);
                startActivity(intent);
            }
        });
        Button btnetc = (Button)findViewById(R.id.etc);
        btnetc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), etc.class);
                startActivity(intent);
            }
        });
    }
}