CREATE TABLE "wounds" (
  "id" SERIAL PRIMARY KEY,
  "patient_id" integer NOT NULL,
  "clinician_id" varchar NOT NULL,
  "device_id" varchar NOT NULL,
  "treated" boolean NOT NULL DEFAULT false
);

CREATE TABLE "treatment_sessions" (
  "notes" varchar,
  "id" SERIAL PRIMARY KEY,
  "wound_id" integer NOT NULL,
  "status_of_device" varchar,
  "drug_volume_required" double precision,
  "laser_power_required" double precision,
  "wash_volume_required" double precision,
  "first_wait" double precision,
  "second_wait" double precision,
  "drug_volume_administered" double precision,
  "wash_volume_administered" double precision,
  "power_delivered_by_laser_1" double precision,
  "power_delivered_by_laser_2" double precision,
  "power_delivered_by_laser_3" double precision,
  "power_delivered_by_laser_4" double precision,
  "estimated_duration_for_drug_administration" double precision,
  "estimated_duration_for_light_administration" double precision,
  "estimated_duration_for_wash_administration" double precision,
  "issues" varchar[],
  "started" boolean NOT NULL DEFAULT false,
  "paused" boolean NOT NULL DEFAULT false,
  "completed" boolean NOT NULL DEFAULT false,
  "date_scheduled" date,
  "start_time_scheduled" timestamp,
  "start_time" timestamp,
  "end_time" timestamp,
  "handshake_random_string" varchar,
  "handshake_counter" integer,
  "session_number" integer NOT NULL,
  "pain_score" integer
);

ALTER TABLE "treatment_sessions" ADD FOREIGN KEY ("wound_id") REFERENCES "wounds" ("id");

ALTER TABLE "treatment_sessions"
ADD "video_call_id" varchar;

ALTER TABLE "treatment_sessions"
ADD "image_urls" varchar[];

ALTER TABLE "treatment_sessions"
ADD "reschedule_requested" boolean DEFAULT false;