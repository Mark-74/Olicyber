package com.andry;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import java.io.IOException;
import org.apache.commons.io.IOUtils;

public class DynamicLoaderService extends IntentService {
    private static final String ACTION_LOAD = "com.andry.action.LOAD";
    private static final String EXTRA_PASSWORD = "com.andry.extra.password";

    public DynamicLoaderService() {
        super("DynamicLoaderService");
    }

    public static void startActionLoad(Context context, String param1) {
        Intent intent = new Intent(context, DynamicLoaderService.class);
        intent.setAction(ACTION_LOAD);
        intent.putExtra(EXTRA_PASSWORD, param1);
        context.startService(intent);
    }

    /* access modifiers changed from: protected */
    public void onHandleIntent(Intent intent) {
        if (intent != null && ACTION_LOAD.equals(intent.getAction())) {
            handleActionFoo(intent.getStringExtra(EXTRA_PASSWORD));
        }
    }

    private void handleActionFoo(String password_key) {
        try {
            byte[] byteArray = IOUtils.toByteArray(getApplicationContext().getAssets().open("enc_payload"));
            XORDecrypt(byteArray, password_key);
            String response = DynamicDecode(byteArray, "decrypt", "EASYPEASY");
            Log.i("FLAG: ", "ptm{" + response + "}");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void XORDecrypt(byte[] data, String key) {
        throw new UnsupportedOperationException("NOT IMPLEMENTED YET! PURE GUESSING!");
    }

    private String DynamicDecode(byte[] callCode, String method, String decode_key) {
        throw new UnsupportedOperationException("NOT IMPLEMENTED YET! PURE GUESSING!");
    }
}
