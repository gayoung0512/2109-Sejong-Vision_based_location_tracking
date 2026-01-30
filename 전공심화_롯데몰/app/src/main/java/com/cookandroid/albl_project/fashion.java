package com.cookandroid.albl_project;

import android.content.ContentResolver;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.charset.Charset;
//import android.support.v7.app.ActionCompatActivity;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import java.io.InputStream;

public class fashion extends AppCompatActivity{

    Button btnSelec,btnSend;
    ImageView imageView;

    static final int PORT = 12000;


    private static final int REQUEST_CODE = 0;
    private static final String infoip = "10.0.2.2";
    static String filename;
    static Bitmap bitmap;

    private Handler mHandler;
    private Socket socket;
    private DataOutputStream dos;
    private DataInputStream dis;
    private String img_path;
    private final Charset UTF8_CHARSET = Charset.forName("UTF-8");

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fashion);

        imageView = (ImageView) findViewById(R.id.imgVwSelected);
        btnSelec = (Button) findViewById(R.id.btnImageSelection);
        btnSend = (Button) findViewById(R.id.btnImageSend);

        btnSelec.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                intent.setType("image/*");
                intent.setAction(Intent.ACTION_GET_CONTENT);
                startActivityForResult(intent,REQUEST_CODE);
            }
        });

        btnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(getApplicationContext(),filename,Toast.LENGTH_SHORT).show();
                connect();
            }
        });

    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data){
        super.onActivityResult(requestCode,resultCode,data);

        if(requestCode==REQUEST_CODE){
            if (resultCode==RESULT_OK){
                Uri uri = data.getData();
                ContentResolver resolver = getContentResolver();
                try {
                    filename = uri.getLastPathSegment();
                    InputStream inputStream = resolver.openInputStream(uri);

                    bitmap = MediaStore.Images.Media.getBitmap(resolver,uri);

                    Bitmap imgBitmap = BitmapFactory.decodeStream(inputStream);
                    imageView.setImageBitmap(imgBitmap);
                    inputStream.close();
                    Toast.makeText(getApplicationContext(),"파일 불러오기 성공",Toast.LENGTH_SHORT).show();

                }catch (Exception e){
                    Toast.makeText(getApplicationContext(),"파일 불러오기 실패",Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    public void connect(){
        mHandler = new Handler();

        Log.w("connect","연결 하는중");
        Thread checkUpdate = new Thread() {
            public void run() {
                /*ByteArrayOutputStream byteArray = new ByteArrayOutputStream();
                imgBitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArray);
                byte[] bytes = byteArray.toByteArray();*/

                // 서버 접속
                try {
                    socket = new Socket(infoip, PORT);
                    Log.w("서버:", "서버 접속됨");
                } catch (IOException e1) {
                    Log.w("서버:", "서버접속못함");
                    e1.printStackTrace();
                }

                Log.w(": ","안드로이드에서 서버로 연결요청");

                /*String getDirectory = Environment.getExternalStorageDirectory()+filename;
                File file = new File(getDirectory);*/

                ByteArrayOutputStream byteArray = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArray);
                byte[] bytes = byteArray.toByteArray();

                try {
                    dos = new DataOutputStream(socket.getOutputStream());
                    dis = new DataInputStream(socket.getInputStream());

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼:", "버퍼생성 잘못됨");
                }
                Log.w("버퍼:","버퍼생성 잘됨");


                try{
                    String mark=null;
                    dos.writeUTF(Integer.toString(bytes.length));
                    dos.flush();

                    dos.write(bytes);
                    dos.flush();

                    img_path = readUTF8(dis);
                    Log.w("img_path",img_path);
                    mark = readUTF8(dis);
                    socket.close();

                }
                catch (Exception e){
                    Log.w("error", "error occur");
                }
            }
        };
        checkUpdate.start();
        try {
            checkUpdate.join();
        }catch (InterruptedException e){

        }
    }
    public String readUTF8 (DataInputStream in) throws IOException {
        int length = in.readInt();
        byte[] encoded = new byte[length];
        in.readFully(encoded, 0, length);
        return new String(encoded, UTF8_CHARSET);
    }


}