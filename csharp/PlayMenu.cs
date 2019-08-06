using MotionDevice.RollerCoaster;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using debug = UnityEngine.Debug;

public class PlayMenu : MonoBehaviour
{

    Dictionary<KeyCode, Action> keyDictionary;

    private PlayManager pm;
    private Transform tr;

    private bool flag_pitch = true;
    private bool flag_yaw = true;
    private bool flag_roll = true;
    private bool flag_surge = true;
    private bool flag_heave = true;
    private bool flag_sway = true;
    private bool flag_pitch2 = true;
    private bool flag_yaw2 = true;
    private bool flag_roll2 = true;
    private bool flag_heave2 = true;
    private bool constant = true;
    private bool flag_S5 = false;

    private float accel_pitch = 0.0f, accel_yaw = 0.0f, accel_roll = 0.0f, accel_surge = 0.0f, accel_heave = 0.0f, accel_sway = 0.0f;

    float timer, fps;
    Stopwatch sw = new Stopwatch();
    public int idx = 0;

    void FlagInit()
    {
        flag_pitch = true;
        flag_yaw = true;
        flag_roll = true;
        flag_surge = true;
        flag_heave = true;
        flag_sway = true;
        flag_pitch2 = true;
        flag_yaw2 = true;
        flag_roll2 = true;
        flag_heave2 = true;
        constant = true;
        flag_S5 = false;
    }

    // Use this for initialization
    void Start()
    {
        pm = GameObject.Find("PlayManager").GetComponent<PlayManager>();
        tr = GameObject.Find("PlayManager").GetComponent<Transform>();
    }

    // Update is called once per frame
    // todo: dictionary.
    void Update()
    {

        PushButton();
        Timer();
        switch (idx)
        {
            case 1:
                S1_Pitch();
                break;
            case 2:
                S1_Yaw();
                break;
            case 3:
                S1_Roll();
                break;
            case 4:
                S1_Surge();
                break;
            case 5:
                S1_Heave();
                break;
            case 6:
                S1_Sway();
                break;
            case 11:
                S2_Pitch();
                break;
            case 12:
                S2_Yaw();
                break;
            case 13:
                S2_Roll();
                break;
            case 14:
                S2_Surge();
                break;
            case 15:
                S2_Heave();
                break;
            case 16:
                S2_Sway();
                break;
            case 21:
                S3_Pitch();
                break;
            case 22:
                S3_Yaw();
                break;
            case 23:
                S3_Roll();
                break;
            case 24:
                S3_Surge();
                break;
            case 25:
                S3_Heave();
                break;
            case 26:
                S3_Sway();
                break;
            case 31:
                S4();
                break;
            case 32:
                S5();
                break;
            case 33:
                S6();
                break;
            case 99:
                Cycle1();
                break;
            case 100:
                Refresh();
                break;
        }
    }

    void PushButton()
    {
        if (Input.GetKeyDown(KeyCode.Keypad0))
        {
            FlagInit();
            idx = 0;
        }
        else if (Input.GetKeyDown(KeyCode.R))
        {
            FlagInit();
            idx = 100;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            FlagInit();
            idx = 1;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            FlagInit();
            idx = 2;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            FlagInit();
            idx = 3;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha4))
        {
            FlagInit();
            idx = 4;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha5))
        {
            FlagInit();
            idx = 5;
        }
        else if (Input.GetKeyDown(KeyCode.Alpha6))
        {
            FlagInit();
            idx = 6;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha1))
        {
            FlagInit();
            idx = 11;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha2))
        {
            FlagInit();
            idx = 12;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha3))
        {
            FlagInit();
            idx = 13;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha4))
        {
            FlagInit();
            idx = 14;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha5))
        {
            FlagInit();
            idx = 15;
        }
        else if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.Alpha6))
        {
            FlagInit();
            idx = 16;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha1))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 21;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha2))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 22;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha3))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 23;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha4))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 24;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha5))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 25;
        }
        else if (Input.GetKey(KeyCode.LeftControl) && Input.GetKeyDown(KeyCode.Alpha6))
        {
            FlagInit();
            pm.timer = 0.0f;
            idx = 26;
        }
        else if (Input.GetKey(KeyCode.LeftAlt) && Input.GetKeyDown(KeyCode.Alpha1))
        {
            FlagInit();
            idx = 31;
        }
        else if (Input.GetKey(KeyCode.LeftAlt) && Input.GetKeyDown(KeyCode.Alpha2))
        {
            FlagInit();
            idx = 32;
        }
        else if (Input.GetKey(KeyCode.LeftAlt) && Input.GetKeyDown(KeyCode.Alpha3))
        {
            FlagInit();
            flag_yaw = false;
            flag_roll = false;
            idx = 33;
        }
        else if (Input.GetKeyDown(KeyCode.F12))
        {
            debug.Log("Stop Time : " + sw.ElapsedMilliseconds.ToString() + " ms");
        }
        else if (Input.GetKeyDown(KeyCode.G))
        {
            FlagInit();
            pm.timer = 120.0f;
            idx = 99;
        }
    }

    float norm(float x)
    {
        if (x >= 330 && x < 360)
            x = 360 - x;
        else if (x > 0 && x <= 30)
            x = -x;

        return x;
    }
    void Pitch(MonoBehaviour m)
    {

    }
    void S1_Pitch()
    {
        if ((-pm.rotNow.x) < 30 && flag_pitch == true)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x - 1.0f, 0.2f);
        else if ((-pm.rotNow.x) >= 30 && flag_pitch == true) flag_pitch = false;
        else if ((-pm.rotNow.x) > -30 && flag_pitch == false)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x + 1.0f, 0.2f);
        else if ((-pm.rotNow.x) <= -30 && flag_pitch == false) flag_pitch = true;
    }

    void S1_Yaw()
    {
        if (flag_S5 == false)
        {
            if (pm.rotNow.y < 120 && flag_yaw == true)
                pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y + 2.0f, 0.2f);
            else if (pm.rotNow.y >= 120 && flag_yaw == true) flag_yaw = false;
            else if (pm.rotNow.y > -120 && flag_yaw == false)
                pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y - 2.0f, 0.2f);
            else if (pm.rotNow.y <= -120 && flag_yaw == false) flag_yaw = true;
        }

        else if (flag_S5 == true)
        {
            if ((pm.rotNow.y) <= 36 && flag_yaw == true)
                pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y + 1.0f, 0.24f);
            else if (pm.rotNow.y > 36 && flag_yaw == true) flag_yaw = false;
            else if (pm.rotNow.y >= -36 && flag_yaw == false)
                pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y - 1.0f, 0.24f);
            else if (pm.rotNow.y < -36 && flag_yaw == false) flag_yaw = true;
        }

    }

    void S1_Roll()
    {
        if ((-pm.rotNow.z) <= 14 && flag_roll == true)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z - 1.0f, 0.1f);
        else if ((-pm.rotNow.z) > 14 && flag_roll == true) flag_roll = false;
        else if ((-pm.rotNow.z) >= -14 && flag_roll == false)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z + 1.0f, 0.1f);
        else if ((-pm.rotNow.z) < -14 && flag_roll == false) flag_roll = true;
    }

    void S1_Surge()
    {
        if (flag_surge == true && pm.transform.position.x <= 1150.0f)
        {
            if (pm.forward_speed >= -0.32f && constant == true) pm.forward_speed = -0.32f;
            else if (pm.forward_speed > -0.75f && constant == false) pm.forward_speed -= 0.002f;
            else if (pm.forward_speed <= -0.75f && constant == false) flag_surge = false;
        }
        else if (flag_surge == true && pm.transform.position.x > 1150.0f) flag_surge = false;
        else if (flag_surge == false && pm.transform.position.x >= 880.0f)
        {
            if (pm.forward_speed <= 0.32f && constant == true) pm.forward_speed = 0.32f;
            else if (pm.forward_speed < 0.75f && constant == false) pm.forward_speed += 0.002f;
            else if (pm.forward_speed >= 0.75f && constant == false) flag_surge = true;
        }
        else if (flag_surge == false && pm.transform.position.x < 880.0f) flag_surge = true;
    }

    void S1_Heave()
    {
        if (pm.posNow.y <= 0.900 && flag_heave == true)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y + 2.0f, 0.004f);
        else if (pm.posNow.y > 0.900 && flag_heave == true) flag_heave = false;
        else if (pm.posNow.y >= -0.900 && flag_heave == false)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y - 2.0f, 0.004f);
        else if (pm.posNow.y < -0.900 && flag_heave == false) flag_heave = true;
    }

    void S1_Sway()
    {
        if (flag_sway == true && pm.transform.position.z <= 1110.0f)
        {
            if (pm.sway_speed > -0.24f && constant == true) pm.sway_speed = -0.24f;
            else if (pm.sway_speed > -0.48f && constant == false) pm.sway_speed -= 0.002f;
            else if (pm.sway_speed <= -0.48f && constant == false) flag_sway = false;
        }
        else if (flag_sway == true && pm.transform.position.z > 1110.0f) flag_sway = false;
        else if (flag_sway == false && pm.transform.position.z >= 970.0f)
        {
            if (pm.sway_speed < 0.24f && constant == true) pm.sway_speed = 0.24f;
            else if (pm.sway_speed < 0.48f && constant == false) pm.sway_speed += 0.002f;
            else if (pm.sway_speed >= 0.48f && constant == false) flag_sway = true;
        }
        else if (flag_sway == false && pm.transform.position.z < 970.0f) flag_sway = true;
    }

    void S2_Pitch()
    {
        if ((-pm.rotNow.x) <= 29 && flag_pitch == true)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x - accel_pitch, 1.0f);
        else if ((-pm.rotNow.x) > 29 && flag_pitch == true) flag_pitch = false;
        else if ((-pm.rotNow.x) >= -29 && flag_pitch == false)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x + accel_pitch, 1.0f);
        else if ((-pm.rotNow.x) < -29 && flag_pitch == false) flag_pitch = true;

        if (flag_pitch2 == true)
        {
            accel_pitch += 0.002f;
            if (accel_pitch >= 0.72f) flag_pitch2 = false;
        }
        else
        {
            accel_pitch -= 0.002f;
            if (accel_pitch <= 0.0f) flag_pitch2 = true;
        }
    }

    void S2_Yaw()
    {
        if ((pm.rotNow.y) <= 120 && flag_yaw == true)
            pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y + accel_yaw, 1.0f);
        else if (pm.rotNow.y > 120 && flag_yaw == true) flag_yaw = false;
        else if (pm.rotNow.y >= -120 && flag_yaw == false)
            pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y - accel_yaw, 1.0f);
        else if (pm.rotNow.y < -120 && flag_yaw == false) flag_yaw = true;

        if (flag_yaw2 == true)
        {
            accel_yaw += 0.0013f;
            if (accel_yaw >= 0.78f) flag_yaw2 = false;
        }
        else
        {
            accel_yaw -= 0.0013f;
            if (accel_yaw <= 0.001f) flag_yaw2 = true;
        }
    }

    void S2_Roll()
    {
        if ((-pm.rotNow.z) <= 14 && flag_roll == true)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z - accel_roll, 1.0f);
        else if ((-pm.rotNow.z) > 14 && flag_roll == true) flag_roll = false;
        else if ((-pm.rotNow.z) >= -14 && flag_roll == false)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z + accel_roll, 1.0f);
        else if ((-pm.rotNow.z) < -14 && flag_roll == false) flag_roll = true;

        if (flag_roll2 == true)
        {
            accel_roll += 0.001f;
            if (accel_roll >= 0.3f) flag_roll2 = false;
        }
        else
        {
            accel_roll -= 0.001f;
            if (accel_roll <= 0.01f) flag_roll2 = true;
        }
    }

    void S2_Surge()
    {
        constant = false;
        S1_Surge();
    }

    void S2_Heave()
    {
        if (pm.posNow.y <= 0.900 && flag_heave == true)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y + accel_heave, 1.0f);
        else if (pm.posNow.y > 0.900 && flag_heave == true) flag_heave = false;
        else if (pm.posNow.y >= -0.900 && flag_heave == false)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y - accel_heave, 1.0f);
        else if (pm.posNow.y < -0.900 && flag_heave == false) flag_heave = true;

        if (flag_heave2 == true)
        {
            accel_heave += 0.00006f;
            if (accel_heave >= 0.018f) flag_heave2 = false;
        }
        else
        {
            accel_heave -= 0.0001f;
            if (accel_heave <= 0.0001f) flag_heave2 = true;
        }
    }

    void S2_Sway()
    {
        constant = false;
        S1_Sway();
    }

    void S3_Pitch()
    {
        if ((-pm.rotNow.x) < 30 && flag_pitch == true)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x - 0.2f - accel_pitch, 1.0f);
        else if ((-pm.rotNow.x) >= 30 && flag_pitch == true) flag_pitch = false;
        else if ((-pm.rotNow.x) > -30 && flag_pitch == false)
            pm.rotNow.x = Mathf.Lerp(pm.rotNow.x, pm.rotNow.x + 0.2f + accel_pitch, 1.0f);
        else if ((-pm.rotNow.x) <= -30 && flag_pitch == false) flag_pitch = true;

        if (pm.timer >= 5.0f && pm.timer <= 14.0f)
        {
            if (flag_pitch2 == true)
            {
                accel_pitch += 0.002f;
                if (accel_pitch >= 0.48f) flag_pitch2 = false;
            }
            else
            {
                accel_pitch -= 0.002f;
                if (accel_pitch <= 0.0f) flag_pitch2 = true;
            }
        }
        else accel_pitch = 0.0f;
    }

    void S3_Yaw()
    {
        if ((pm.rotNow.y) <= 120 && flag_yaw == true)
            pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y + 0.4f + accel_yaw, 1.0f);
        else if (pm.rotNow.y > 120 && flag_yaw == true) flag_yaw = false;
        else if (pm.rotNow.y >= -120 && flag_yaw == false)
            pm.rotNow.y = Mathf.Lerp(pm.rotNow.y, pm.rotNow.y - 0.4f - accel_yaw, 1.0f);
        else if (pm.rotNow.y < -120 && flag_yaw == false) flag_yaw = true;

        if (pm.timer >= 5.0f && pm.timer <= 14.0f)
        {
            if (flag_yaw2 == true)
            {
                accel_yaw += 0.0015f;
                if (accel_yaw >= 0.36f) flag_yaw2 = false;
            }
            else
            {
                accel_yaw -= 0.0015f;
                if (accel_yaw <= 0.0f) flag_yaw2 = true;
            }
        }
        else accel_yaw = 0.0f;
    }

    void S3_Roll()
    {
        if ((-pm.rotNow.z) <= 14 && flag_roll == true)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z - 0.1f - accel_roll, 1.0f);
        else if ((-pm.rotNow.z) > 14 && flag_roll == true) flag_roll = false;
        else if ((-pm.rotNow.z) >= -14 && flag_roll == false)
            pm.rotNow.z = Mathf.Lerp(pm.rotNow.z, pm.rotNow.z + 0.1f + accel_roll, 1.0f);
        else if ((-pm.rotNow.z) < -14 && flag_roll == false) flag_roll = true;

        if (pm.timer >= 5.0f && pm.timer <= 14.0f)
        {
            if (flag_roll2 == true)
            {
                accel_roll += 0.0005f;
                if (accel_roll >= 0.12f) flag_roll2 = false;
            }
            else
            {
                accel_roll -= 0.005f;
                if (accel_roll <= 0.00f) flag_roll2 = true;
            }
        }
        else accel_roll = 0.0f;
    }

    void S3_Surge()
    {
        if (pm.timer >= 0.0f && pm.timer <= 10.0f)
            constant = false;
        else constant = true;
        if (flag_surge == true && pm.transform.position.x <= 1150.0f)
        {
            if (pm.forward_speed >= -0.32f && constant == true) pm.forward_speed = -0.32f;
            else if (pm.forward_speed > -0.75f && constant == false) pm.forward_speed -= 0.006f;
            else if (pm.forward_speed <= -0.75f && constant == false) flag_surge = false;
        }
        else if (flag_surge == true && pm.transform.position.x > 1150.0f) flag_surge = false;
        else if (flag_surge == false && pm.transform.position.x >= 880.0f)
        {
            if (pm.forward_speed <= 0.32f && constant == true) pm.forward_speed = 0.32f;
            else if (pm.forward_speed < 0.75f && constant == false) pm.forward_speed += 0.006f;
            else if (pm.forward_speed >= 0.75f && constant == false) flag_surge = true;
        }
        else if (flag_surge == false && pm.transform.position.x < 880.0f) flag_surge = true;
    }

    void S3_Heave()
    {
        if (pm.posNow.y < 1.0f && flag_heave == true)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y + 0.008f + accel_heave, 1.0f);
        else if (pm.posNow.y >= 1.0f && flag_heave == true) flag_heave = false;
        else if (pm.posNow.y > -1.0f && flag_heave == false)
            pm.posNow.y = Mathf.Lerp(pm.posNow.y, pm.posNow.y - 0.008f - accel_heave, 1.0f);
        else if (pm.posNow.y <= -1.0f && flag_heave == false) flag_heave = true;

        if (pm.timer >= 0.0f && pm.timer <= 10.0f)
        {
            if (flag_heave2 == true)
            {
                accel_heave += 0.00006f;
                if (accel_heave >= 0.018f) flag_heave2 = false;
            }
            else
            {
                accel_heave -= 0.0001f;
                if (accel_heave <= 0.0001f) flag_heave2 = true;
            }
        }
        else accel_heave = 0.0f;
    }

    void S3_Sway()
    {
        if (pm.timer >= 0.0f && pm.timer <= 10.0f)
            constant = false;
        else constant = true;
        if (flag_sway == true && pm.transform.position.z <= 1110.0f)
        {
            if (pm.sway_speed > -0.24f && constant == true) pm.sway_speed = -0.24f;
            else if (pm.sway_speed > -0.48f && constant == false) pm.sway_speed -= 0.002f;
            else if (pm.sway_speed <= -0.48f && constant == false) flag_sway = false;
        }
        else if (flag_sway == true && pm.transform.position.z > 1110.0f) flag_sway = false;
        else if (flag_sway == false && pm.transform.position.z >= 970.0f)
        {
            if (pm.sway_speed < 0.24f && constant == true) pm.sway_speed = 0.24f;
            else if (pm.sway_speed < 0.48f && constant == false) pm.sway_speed += 0.002f;
            else if (pm.sway_speed >= 0.48f && constant == false) flag_sway = true;
        }
        else if (flag_sway == false && pm.transform.position.z < 970.0f) flag_sway = true;
    }


    void S4()
    {
        S1_Pitch();
        if (flag_surge == true && pm.transform.position.x <= 1200.0f)
        {
            if (pm.forward_speed >= -0.3f) pm.forward_speed = -0.3f;
        }
        else if (flag_surge == true && pm.transform.position.x > 1200.0f) flag_surge = false;
        else if (flag_surge == false && pm.transform.position.x >= 880.0f)
        {
            if (pm.forward_speed <= 0.3f) pm.forward_speed = 0.3f;
        }
        else if (flag_surge == false && pm.transform.position.x < 880.0f) flag_surge = true;
    }

    void S5()
    {
        flag_S5 = true;
        S1_Yaw();
        S1_Roll();
        S1_Surge();
    }

    void S6()
    {
        flag_S5 = true;
        S1_Pitch();
        S1_Yaw();
        S1_Roll();
        S1_Surge();
    }

    public void Timer()
    {
        timer += Time.deltaTime;
    }

    void Refresh()
    {
        if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
            pm.recentering = true;
    }

    void Cycle1()
    {
        if (pm.timer >= 0.0f && pm.timer < 60.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 60.0f && pm.timer < 80.0f)
        {
            S1_Pitch();
        }
        else if (pm.timer >= 80.0f && pm.timer < 100.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S1_Yaw();
        }
        else if (pm.timer >= 100.0f && pm.timer < 120.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S1_Roll();
        }
        else if (pm.timer >= 120.0f && pm.timer < 143.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S1_Surge();
        }
        else if (pm.timer >= 143.0f && pm.timer < 155.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S1_Heave();
        }
        else if (pm.timer >= 155.0f && pm.timer < 175.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S1_Sway();
        }
        else if (pm.timer >= 175.0f && pm.timer < 235.0f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 235.0f && pm.timer < 248.5f)
        {
            S2_Pitch();
        }
        else if (pm.timer >= 248.5f && pm.timer < 270.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S2_Yaw();
        }
        else if (pm.timer >= 270.5f && pm.timer < 290.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S2_Roll();
        }
        else if (pm.timer >= 290.5f && pm.timer < 314.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S2_Surge();
        }
        else if (pm.timer >= 314.5f && pm.timer < 334.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S2_Heave();
        }
        else if (pm.timer >= 334.5f && pm.timer < 353.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S2_Sway();
        }
        else if (pm.timer >= 353.5f && pm.timer < 413.5f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 413.5f && pm.timer < 431.5f)
        {
            S3_Pitch();
        }
        else if (pm.timer >= 431.5f && pm.timer < 457.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S3_Yaw();
        }
        else if (pm.timer >= 457.9f && pm.timer < 477.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S3_Roll();
        }
        else if (pm.timer >= 477.9f && pm.timer < 497.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S3_Surge();
        }
        else if (pm.timer >= 497.9f && pm.timer < 517.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S3_Heave();
        }
        else if (pm.timer >= 517.9f && pm.timer < 537.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            if (pm.recentering == false)
                S3_Sway();
        }
        else if (pm.timer >= 537.9f && pm.timer < 607.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 607.9f && pm.timer < 667.9f)
        {
            S4();
        }
        else if (pm.timer >= 667.9f && pm.timer < 727.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 727.9f && pm.timer < 787.9f)
        {
            S5();
        }
        else if (pm.timer >= 787.9f && pm.timer < 847.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
        }
        else if (pm.timer >= 847.9f && pm.timer < 907.9f)
        {
            S6();
        }
        else if (pm.timer >= 907.9f)
        {
            if (pm.rotNow != Vector3.zero && tr.position != new Vector3(928.0f, 54.0f, 1020.0f))
                pm.recentering = true;
            FlagInit();
            idx = 0;
        }
    }
}
