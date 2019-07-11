using MotionDevice.RollerCoaster;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEngine;
using UTJ.FrameCapturer;



public class CalQ : MonoBehaviour
{
	public float pitchDelta, yawDelta, rollDelta, surgeDelta, heaveDelta, swayDelta, tmpHeave; // to observe data
	public int frameMax = 601; // 60 fps * 60 sec

	#region inner_types
	#endregion

	#region fields
	private Vector3 prevVector;
	PlayManager playManager;
	PlayMenu playMenu;
	MovieRecorder mRecoder;
	readonly string DATA_PATH = "../analysis/data/raw/motion/motion_dist_raw.txt";
	readonly string META_PATH = "../analysis/data/raw/motion/motion_dist_raw.meta";
	List<int[]> totalBins = new List<int[]>();
	bool flag = false;
	bool timerFlag = false;
	int frame = 0;
	int startVideoFrame;
	int idx = 0;
	int target = 60;
	float pitchPrev, yawPrev, rollPrev;
	float timer = 0.0f;

	#endregion

	const int PITCH = 0, YAW = 1, ROLL = 2, SURGE = 3, HEAVE = 4, SWAY = 5;
	const float PITCH_MAX = 13.5f, YAW_MAX = 14.6f, ROLL_MAX = 5.6f, SURGE_MAX = 14.0f, HEAVE_MAX = 0.32f, SWAY_MAX = 9.0f;
	readonly float[] PITCH_BIN = { - PITCH_MAX * 4 / 5, - PITCH_MAX * 1 / 5, PITCH_MAX * 1/5, PITCH_MAX * 4 / 5 };
	readonly float[] YAW_BIN = { -YAW_MAX * 4 / 5, -YAW_MAX * 1 / 5, YAW_MAX * 1 / 5, YAW_MAX * 4 / 5 };
	readonly float[] ROLL_BIN = { -ROLL_MAX * 4 / 5, -ROLL_MAX * 1 / 5, ROLL_MAX * 1 / 5, ROLL_MAX * 4 / 5 };
	readonly float[] SURGE_BIN = { -SURGE_MAX * 4 / 5, -SURGE_MAX * 1 / 5, SURGE_MAX * 1 / 5, SURGE_MAX * 4 / 5 };
	readonly float[] HEAVE_BIN = { -HEAVE_MAX * 4 / 5, -HEAVE_MAX * 1 / 5, HEAVE_MAX * 1 / 5, HEAVE_MAX * 4 / 5 };
	readonly float[] SWAY_BIN = { -SWAY_MAX * 4 / 5, -SWAY_MAX * 1 / 5, SWAY_MAX * 1 / 5, SWAY_MAX * 4 / 5 };



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

		if (mRecoder.getFrame - startVideoFrame == frameMax + 1)
//			if (mRecoder.getFrame - startVideoFrame == 3601)
			mRecoder.EndRecording();

		if (flag == true)
		{
			if ((frame % 20) == 0)
			{
				prevVector = new Vector3(playManager.tr.position.x, playManager.posNow.y, playManager.tr.position.z);
				pitchPrev = playManager.rotNow.x;
				yawPrev = playManager.rotNow.y;
				rollPrev = playManager.rotNow.z;

			}
			else if ((frame % 20) == 19)
			{

				pitchDelta = playManager.rotNow.x - pitchPrev;
				yawDelta = playManager.rotNow.y - yawPrev;
            rollDelta = playManager.rotNow.z - rollPrev;
				surgeDelta = playManager.tr.position.x - prevVector.x;
				heaveDelta = playManager.posNow.y - prevVector.y;
				swayDelta = playManager.tr.position.z - prevVector.z;
				totalBins.Add(ToCategory(pitchDelta, yawDelta, rollDelta, surgeDelta, heaveDelta, swayDelta));
			}
			frame++;
		}

		if ((frame > frameMax) && (flag == true)) Finish();
	}

	#region select_bin 
	int[] ToCategory(float pitchDelta, float yawDelta, float rollDelta, float surgeDelta, float heaveDelta, float swayDelta)
	{
		return new int[] { ToCategoryImpl(pitchDelta, 0), ToCategoryImpl(yawDelta, 1), ToCategoryImpl(rollDelta, 2),
			ToCategoryImpl(surgeDelta, 3), ToCategoryImpl(heaveDelta, 4), ToCategoryImpl(swayDelta, 5) };
	}

	int ToCategoryImpl(float delta, int axis)
	{
 		switch (axis)
		{
			case PITCH:
				if (delta <= PITCH_BIN[2] && delta >= PITCH_BIN[1] ) return 0; // low level motion
				else if (delta <= PITCH_BIN[3] && delta > PITCH_BIN[2] ) return 1; // medium level motion
				else if (delta < PITCH_BIN[1] && delta >= PITCH_BIN[0] ) return 2; // medium level motion
				else if (delta > PITCH_BIN[3] ) return 3; // high level motion
				else return 4; // high level motion
			case YAW:
				if (delta <= YAW_BIN[2] && delta >= YAW_BIN[1]) return 0; // low level motion
				else if (delta <= YAW_BIN[3] && delta > YAW_BIN[2]) return 1; // medium level motion
				else if (delta < YAW_BIN[1] && delta >= YAW_BIN[0]) return 2; // medium level motion
				else if (delta > YAW_BIN[3]) return 3; // high level motion
				else return 4; // high level motion
			case ROLL:
				if (delta <= ROLL_BIN[2] && delta >= ROLL_BIN[1]) return 0; // low level motion
				else if (delta <= ROLL_BIN[3] && delta > ROLL_BIN[2]) return 1; // medium level motion
				else if (delta < ROLL_BIN[1] && delta >= ROLL_BIN[0]) return 2; // medium level motion
				else if (delta > ROLL_BIN[3]) return 3; // high level motion
				else return 4; // high level motion
			case SURGE:
				if (delta <= SURGE_BIN[2] && delta >= SURGE_BIN[1]) return 0; // low level motion
				else if (delta <= SURGE_BIN[3] && delta > SURGE_BIN[2]) return 1; // medium level motion
				else if (delta < SURGE_BIN[1] && delta >= SURGE_BIN[0]) return 2; // medium level motion
				else if (delta > SURGE_BIN[3]) return 3; // high level motion
				else return 4; // high level motion
			case HEAVE:
				if (delta <= HEAVE_BIN[2] && delta >= HEAVE_BIN[1]) return 0; // low level motion
				else if (delta <= HEAVE_BIN[3] && delta > HEAVE_BIN[2]) return 1; // medium level motion
				else if (delta < HEAVE_BIN[1] && delta >= HEAVE_BIN[0]) return 2; // medium level motion
				else if (delta > HEAVE_BIN[3]) return 3; // high level motion
				else return 4; // high level motion
			case SWAY:
				if (delta <= SWAY_BIN[2] && delta >= SWAY_BIN[1]) return 0; // low level motion
				else if (delta <= SWAY_BIN[3] && delta > SWAY_BIN[2]) return 1; // medium level motion
				else if (delta < SWAY_BIN[1] && delta >= SWAY_BIN[0]) return 2; // medium level motion
				else if (delta > SWAY_BIN[3]) return 3; // high level motion
				else return 4; // high level motion
			default:
				return -1; // error occured
		}
	}

	#endregion

	void Write_File()
	{
		string dataPath = DATA_PATH;
		string metaPath = META_PATH;

		using (var writer = new StreamWriter(dataPath, true, Encoding.UTF8))
		{
			foreach (int[] bin in totalBins)
				for (int i = 0; i < bin.Length; i++) writer.Write(string.Format("{0} ", bin[i]));
		}

		StreamWriter metaWriter = new StreamWriter(metaPath, true);
		metaWriter.Write(idx + " ");
		metaWriter.Write(playManager.timer + " ");
		metaWriter.Write(frame );
		metaWriter.Close();
	}

	void Finish()
	{
		Debug.Log("Good luck!");
		Write_File();
		playMenu.idx = 0;
		flag = false;
	}
}
