using MotionDevice.RollerCoaster;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;
using UTJ.FrameCapturer;

public class CalQ : MonoBehaviour
{

	public int[] counts = new int[625];
	public int target = 60;

	#region inner_types
	#endregion

	#region fields
	PlayManager playManager;
	PlayMenu playMenu;
	MovieRecorder mRecoder;
	RecorderBase recorderBase;
	[SerializeField]
	readonly string DATA_PATH = "../analysis/data/raw/motion/motion_dist_raw.txt";
	[SerializeField]
	readonly string META_PATH = "../analysis/data/raw/motion/motion_dist_raw.meta";
	List<int[]> countsTotal = new List<int[]>();
	bool flag = false;
	bool timerFlag = false;
	int frameMax = 3589;
	int frame = 0;
	int startVideoFrame;
	int idx = 0;
	float pitchPrev = 0.0f;
	float yawPrev = 0.0f;
	float rollPrev = 0.0f;
	float heavePrev = 0.0f;
	float timer = 0.0f;
	#endregion

	void Start()
	{
		Application.targetFrameRate = target;
		playManager = GameObject.Find("PlayManager").GetComponent<PlayManager>();
		playMenu = GameObject.Find("PlayManager").GetComponent<PlayMenu>();
		mRecoder = GameObject.Find("Fove Interface").GetComponent<MovieRecorder>();
		frame = 0;
	}

   void FixedUpdate()
	{
		if (!(Application.targetFrameRate == target))
			Application.targetFrameRate = target;
		if (playMenu.idx != 0 && idx == 0)
		{
			flag = true;
			idx = playMenu.idx;
			mRecoder.BeginRecording();
			startVideoFrame = mRecoder.getFrame;
		}

		if (timerFlag == true) timer += Time.deltaTime;

		if (mRecoder.getFrame - startVideoFrame == 3601)
			mRecoder.EndRecording();

		if (flag == true)
		{
			int binNo;
			if ((frame % 60) == 0)
			{
				pitchPrev = playManager.rotNow.x;
				yawPrev = playManager.rotNow.y;
				rollPrev = playManager.rotNow.z;
				heavePrev = playManager.posNow.y;
			}
			else if ((frame % 60) == 3)
			{

				binNo = SelectBin(playManager.rotNow.x - pitchPrev,
										playManager.rotNow.y - yawPrev,
										playManager.rotNow.z - rollPrev,
										playManager.posNow.y - heavePrev);
				counts[binNo] = counts[binNo] + 1;
				countsTotal.Add((int[])counts.Clone());
			}
			else if ((frame % 60) == 20)
			{
				pitchPrev = playManager.rotNow.x;
				yawPrev = playManager.rotNow.y;
				rollPrev = playManager.rotNow.z;
				heavePrev = playManager.posNow.y;
			}
			else if ((frame % 60) == 23)
			{
				binNo = SelectBin(playManager.rotNow.x - pitchPrev,
										playManager.rotNow.y - yawPrev,
										playManager.rotNow.z - rollPrev,
										playManager.posNow.y - heavePrev);
				counts[binNo] = counts[binNo] + 1;
				countsTotal.Add((int[])counts.Clone());
			}
			else if ((frame % 60) == 40)
			{
				pitchPrev = playManager.rotNow.x;
				yawPrev = playManager.rotNow.y;
				rollPrev = playManager.rotNow.z;
				heavePrev = playManager.posNow.y;
			}
			else if ((frame % 60) == 43)
			{
				binNo = SelectBin(playManager.rotNow.x - pitchPrev,
										playManager.rotNow.y - yawPrev,
										playManager.rotNow.z - rollPrev,
										playManager.posNow.y - heavePrev);
				counts[binNo] = counts[binNo] + 1;
				countsTotal.Add((int[])counts.Clone());
			}
			frame++;
		}

		if ((frame > frameMax) && (flag == true)) Finish();
		// playManager.timer >= 60.0f && flag == true)
	}

	#region select_bin 
	int SelectBin(float pitch, float yaw, float roll, float heave)
	{
		return SelectionPitch(pitch) + SelectionYaw(yaw)
			 + SelectionRoll(roll) + SelectionHeave(heave);
	}

	int SelectionPitch(float pitch)
	{
		int tmp = 0;
		if (pitch <= 0.00005f && pitch >= -0.00005f) ;
		else if (pitch <= 0.61f && pitch > 0.00005f) tmp += 125;
		else if (pitch >= -0.61f && pitch < -0.00005f) tmp += 250;
		else if (pitch > 0.61f) tmp += 375;
		else if (pitch < -0.61f) tmp += 500;
		return tmp;
	}

	int SelectionYaw(float yaw)
	{
		int tmp = 0;
		if (yaw <= 0.00005f && yaw >= -0.00005f) ;
		else if (yaw <= 0.61f && yaw > 0.00005f) tmp += 25;
		else if (yaw >= -0.61f && yaw < -0.00005f) tmp += 50;
		else if (yaw > 0.61f) tmp += 75;
		else if (yaw < -0.61f) tmp += 100;
		return tmp;
	}

	int SelectionRoll(float roll)
	{
		int tmp = 0;
		if (roll <= 0.00005f && roll >= -0.00005f) ;
		else if (roll <= 0.61f && roll > 0.00005f) tmp += 5;
		else if (roll >= -0.61f && roll < -0.00005f) tmp += 10;
		else if (roll > 0.61f) tmp += 15;
		else if (roll < -0.61f) tmp += 20;
		return tmp;
	}

	int SelectionHeave(float heave)
	{
		int tmp = 0;
		if (heave <= 0.00005f && heave >= -0.00005f) ;
		else if (heave <= 0.61f && heave > 0.00005f) tmp += 1;
		else if (heave >= -0.61f && heave < -0.00005f) tmp += 2;
		else if (heave > 0.61f) tmp += 3;
		else if (heave < -0.61f) tmp += 4;
		return tmp;
	}
	#endregion

	void Write_File()
	{
		string dataPath = DATA_PATH;
		string metaPath = META_PATH;
		StreamWriter dataWriter = new StreamWriter(dataPath, true);
		foreach (int[] counts in countsTotal)
			for (int i = 0; i < counts.Length; i++) dataWriter.Write(counts[i] + " ");
		dataWriter.Close();
		StreamWriter metaWriter = new StreamWriter(metaPath, true);
		metaWriter.Write(idx + " ");
		metaWriter.Write(playManager.timer + " ");
		metaWriter.Write(frame );
		metaWriter.Close();
	}

	void Finish()
	{
		Debug.Log("hi");
		Write_File();
		playMenu.idx = 0;
		flag = false;
	}
}
