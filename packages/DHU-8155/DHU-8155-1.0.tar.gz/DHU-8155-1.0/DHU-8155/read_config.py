import yaml
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.yaml")

class ReadConfig:
    def __init__(self):
        yaml.warnings({'YAMLLoadWarning': False})
        f = open(configPath, 'r', encoding='utf-8')  # 打开yaml文件
        cfg = f.read()
        d = yaml.load(cfg)
        self.data = d


    def get_canoe(self, name):
        return self.data['CANOE'][name]

    def get_signal(self, name):
        return self.data['SIGNAL'][name]

    def get_usgmodsts_val(self, name):
        return self.data['USGMODSTS_VAL'][name]

    def get_time(self, name):
        return self.data['TIME'][name]

    def get_adapt_api(self, name):
        return self.data['ADAPT_API'][name]

    ###################################################################################################以下王家峰
    '''P档位解锁'''

    def get_p_gear_unlock(self, name):
        return self.data['P_GEAR_ULOCK'][name]

    '''外后视镜倾斜'''

    def get_extr_mirr_tilt(self, name):
        return self.data['EXTR_MIRR_TILT'][name]

    '''外后视镜选择'''

    def get_extr_mirr_adjust(self, name):
        return self.data['EXTR_MIRR_ADJUST'][name]

    def get_sun_roof_curtain(self, name):
        return self.data['SUN_ROOF_CURTAIN'][name]

    '''自动关闭车窗'''

    def get_cls_aut_window(self, name):
        return self.data['CLS_AUT_WINDOW'][name]

    '''临时警戒解除'''

    def get_setting_reduced_guard(self, name):
        return self.data['SETTING_FUNC_REDUCED_GUARD'][name]

    '''被动报警'''

    def get_passive_arming(self, name):
        return self.data['PASSIVE_ARMING'][name]

    '''找车提醒'''

    def get_locator_remider_mode(self, name):
        return self.data['LOCATOR_REMINDER_MODE'][name]

    '''拖车灯开关'''

    def get_trailer_lamp(self, name):
        return self.data['TRAILER_LAMP'][name]

    '''拖车灯自动检查'''

    def get_trailer_lamp_auto_check(self, name):
        return self.data['TRAILER_LAMP_AUTO_CHECK'][name]

    '''滑行开关'''

    def get_sailing_switch(self, name):
        return self.data['SAILING_SWITCH'][name]

    '''充电盖'''

    def get_charging_cap(self, name):
        return self.data['CHARGING_CAP'][name]

    '''空调电源总开关'''

    def get_havc_func_power(self, name):
        return self.data['HAVC_FUNC_POWER'][name]

    '''温度控制'''

    def get_havc_func_temp(self, name):
        return self.data['HAVC_FUNC_TEMP'][name]

    '''双区同步'''

    def get_havc_func_temp_dual(self, name):
        return self.data['HAVC_FUNC_TEMP_DUAL'][name]

    '''G-CLEAN'''

    def get_havc_func_g_clean(self, name):
        return self.data['HAVC_FUNC_G_CLEAN'][name]

    '''吹风模式'''

    def get_havc_func_blowing_mode(self, name):
        return self.data['HAVC_FUNC_BLOWING_MODE'][name]

    '''自动'''

    def get_havc_func_auto(self, name):
        return self.data['HAVC_FUNC_AUTO'][name]

    '''压缩机AC'''

    def get_havc_func_ac(self, name):
        return self.data['HAVC_FUNC_AC'][name]

    '''循环模式'''

    def get_havc_func_circulation(self, name):
        return self.data['HAVC_FUNC_CIRCULATION'][name]

    '''手动风量风速'''

    def get_havc_func_fan_speed(self, name):
        return self.data['HAVC_FUNC_FAN_SPEED'][name]

    '''自动风量风速'''

    def get_havc_func_auto_fan_speed(self, name):
        return self.data['HAVC_FUNC_AUTO_FAN_SPEED'][name]

    '''MAX_AC'''

    def get_havc_func_ac_max(self, name):
        return self.data['HAVC_FUNC_AC_MAX'][name]

    '''手动方向盘加热'''

    def get_havc_steer_wheel_heat(self, name):
        return self.data['HAVC_STEER_WHEEL_HEAT'][name]

    '''自动方向盘加热'''

    def get_havc_auto_steer_wheel_heat(self, name):
        return self.data['HAVC_AUTO_STEER_WHEEL_HEAT'][name]

    '''室内空气净化'''

    def get_havc_air_cleaner(self, name):
        return self.data['HAVC_AUTO_AIR_CLEANER'][name]

    '''前排自动除霜除雾'''

    def get_havc_auto_defrost_front(self, name):
        return self.data['HAVC_AUTO_DEFROST_FRONT'][name]

    '''舒适性关窗提醒'''

    def get_havc_auto_close_widow_remind(self, name):
        return self.data['HAVC_AUTO_CLOSE_WINDOW_REMIND'][name]

    '''座椅通风档位'''

    def get_havc_seat_vent_level(self, name):
        return self.data['HAVC_SEAT_VENT_LEVEL'][name]

    '''座椅通风时间'''

    def get_havc_auto_seat_vent_time(self, name):
        return self.data['HAVC_AUTO_SEAT_VENT_TIME'][name]

    '''情景模式ECO'''

    def get_havc_eco_switch(self, name):
        return self.data['HAVC_ECO_SWITCH'][name]

    '''空调总开关   climate power'''

    def get_climate_power(self, name):
        return self.data['CLIMATE_POWER'][name]

    '''座椅加热档位'''

    def get_havc_seat_heating(self, name):
        return self.data['HAVC_SEAT_HEATING'][name]

    '''最大除霜'''

    def get_havc_defrost_front_max(self, name):
        return self.data['HAVC_FUNC_DEFROST_FRONT_MAX'][name]

    # '''驾驶模式之经济模式'''
    # def get_drive_mode_selection_eco(self, name):
    #     return self.data['DRIVE_MODE_SELECTION_ECO'][name]

    '''驾驶模式之舒适模式'''

    def get_drive_mode_selection_comfort(self, name):
        return self.data['DRIVE_MODE_SELECTION_COMFORT'][name]

    '''驾驶模式之全越野模式'''

    def get_drive_mode_selection_offroad(self, name):
        return self.data['DRIVE_MODE_SELECTION_OFFROAD'][name]

    '''驾驶模式之雪地模式'''

    def get_drive_mode_selection_snow(self, name):
        return self.data['DRIVE_MODE_SELECTION_SNOW'][name]

    '''驾驶模式之沙地模式'''

    def get_drive_mode_selection_sand(self, name):
        return self.data['DRIVE_MODE_SELECTION_SAND'][name]

    '''驾驶模式之泥地模式'''

    def get_drive_mode_selection_mud(self, name):
        return self.data['DRIVE_MODE_SELECTION_MUD'][name]

    '''驾驶模式之岩石模式'''

    def get_drive_mode_selection_rock(self, name):
        return self.data['DRIVE_MODE_SELECTION_ROCK'][name]

###################################################################################################以下黄宏凯

    ##间接生命探测    life detection
    def get_life_detection_OTHER(self, name):
        return self.data['LIFE_DETECTION_OTHER'][name]

    # BEV Power开关    bev power
    def get_bev_power(self, name):
        return self.data['BEV_POWER'][name]

    # 主动悬架  activesuspension
    def get_active_suspension(self, name):
        return self.data['ACTIVE_SUSPENSION'][name]

    # 低速报警音开关   low speed alarm tone
    def get_low_speed_alarm_tone(self, name):
        return self.data['LOW_SPEED_ALARM_TONE'][name]

    # 方向盘位置调节    steering wheel position adjustment
    def get_steering_wheel_position_adjustment(self, name):
        return self.data['STEERING_WHEEL_POSITION_ADJUSTMENT'][name]

    # 电动安全带         electric seat belt
    def get_electric_seat_belt(self, name):
        return self.data['ELECTRIC_SEAT_BELT'][name]

    def get_pass(self, name):
        return self.data['ELECTRIC_SEAT_BELT_PASS'][name]

    # 能量回收等级        energy recovery level
    def get_energy_recovery_level(self, name):
        return self.data['ENERGY_RECOVERY_LEVEL'][name]

    # 自动驻车          automatic parking
    def get_automatic_parking(self, name):
        return self.data['AUTOMATIC_PARKING'][name]

    # 陡坡缓降    steep slope
    def get_steep_slope(self, name):
        return self.data['STEEP_SLOPE'][name]

    #EPB Auto
    def get_epb_auto(self, name):
        return self.data['EPB_Auto'][name]

    #   交通标志识别TSI    traffic sign recognition
    # def get_traffic_sign_recognition(self, name):
    #    return self.data['TRAFFIC_SIGN_RECOGNITION'][name]

    # 启停       stop_start
    def get_stop_start(self, name):
        return self.data['STOP_START'][name]

    # ESC_SPORT
    def get_esc_sport(self, name):
        return self.data['ESC_SPORT_MODE'][name]

    # 电池模式
    def get_battery_mode(self, name):
        return self.data['BATTERY_MODE'][name]

    # 童锁
    def get_child_lock(self, name):
        return self.data['CHILD_LOCK'][name]

    # 前雨刮维护位置
    def get_front_wiper_maintenance_position(self, name):
        return self.data['FRONT_WIPER_MAINTENANCE_POAITION'][name]

    # wpc
    def get_wpc_switch(self, name):
        return self.data['WPC_SWITCH'][name]

    # 自动除湿

    def get_auto_humidity(self, name):
        return self.data['AUTO_HUMIDITY'][name]

    # 内循环

    def get_recirc_switch(self, name):
        return self.data['RECIRC_SWITCH'][name]

    # # 空调总开关   climate power
    #
    # def get_climate_power(self, name):
    #     return self.data['CLIMATE_POWER'][name]

    # AC

    def get_climate_compressor(self, name):
        return self.data['CLIMATE_COMPRESSOR'][name]

    # E_PEDAL

    def get_e_Pedal(self, name):
        return self.data['E_PEDAL'][name]

    # 节油模式

    def get_fuel_saving_mode(self, name):
        return self.data['FUEL_SAVING_MODE'][name]

    # 驾驶模式     drive mode

    def get_drive_mode(self, name):
        return self.data['DRIVE_MODE'][name]

    # 驾驶模式之经济模式

    def get_drive_mode_selection_eco(self, name):
        return self.data['DRIVE_MODE_SELECTION_ECO'][name]

    # CarV2X报警设置

    def get_safety_alarm(self, name):
        return self.data['SAFETY_ALARM'][name]

    # 驾驶模式个性化

    def get_drive_mode_individual(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL'][name]

    # 个性化模式-RAB

    def get_drive_mode_individual_rab(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_RAB'][name]

    # 个性化模式-Propulsion

    def get_drive_mode_individual_propulsion(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_PROPULSION'][name]

    # 个性化模式-Air conditioner(Climate) setting

    def get_drive_mode_individual_climate(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_CLIMATE'][name]

    # 个性化模式-Steering wheel assist level setting

    def get_drive_mode_individual_Steeringwheel(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_WHEEL'][name]

    # 个性化模式-Engine StartStop
    def get_drive_mode_individual_Enginestartstop(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_BPF'][name]

    # 个性化模式-Suspension settings
    def get_drive_mode_individual_Suspensionsettings(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_SUSPENSION'][name]

    # 个性化模式-Active rear spoiler setting
    def get_drive_mode_individual_Rearspoiler(self, name):
        return self.data['DRIVE_MODE_INDIVIDUAL_REARSPOILER'][name]

    # 车内模拟声浪开关
    def get_artificial_sound(self, name):
        return self.data['ARTIFICIAL_SOUND'][name]

    # 车内模拟声浪模式选择
    def get_artificial_sound_type(self, name):
        return self.data['ARTIFICIAL_SOUND_TYPE'][name]

    # 车内模拟声浪预览(预览声浪ON  & 暂停预览OFF)
    def get_artificial_sound_preview(self, name):
        return self.data['ARTIFICIAL_SOUND_PREVIEW'][name]

    #托车模式软按键
    def get_trailer_mode(self, name):
        return self.data['TRAILER_MODE'][name]

    # G-Clean
    def get_g_clean(self, name):
        return self.data['G_CLEAN'][name]

    # 空气质量IAQC
    def get_aqs_switch(self, name):
        return self.data['AQS_SWITCH'][name]

    # CO2监测开关
    def get_co2_switch(self, name):
        return self.data['CO2_SWITCH'][name]

    #PM2.5车内空气净化
    def get_auto_ions_switch(self, name):
        return self.data['AUTO_ION_SWITCH'][name]

    # 空气净化器档位
    def get_acc_level(self, name):
        return self.data['AAC_LEVEL'][name]

    # 香氛等级
    def get_air_frageance(self, name):
        return self.data['AIR_FRAGRANCE_LEVEL'][name]

    # 日夜主题切换
    def get_brightnss_day(self, name):
        return self.data['BRIGHTNESS_DAY'][name]

    # 背光亮度日夜模式选择
    def get_brightnss_daymode(self, name):
        return self.data['BRIGHTNESS_DAYMODE'][name]

    #智能除异味
    def get_intelligent_deodorization(self, name):
        return self.data['INTELLIGENT_DEODORIZATION'][name]

    # 最大除霜
    def get_defrost_front_max(self, name):
        return self.data['DEFROST_FRONT_MAX'][name]

    # TCAM复位
    def get_tcam_reset(self, name):
        return self.data['TCAM_RESET'][name]

    # RVDC
    def get_rvdc(self, name):
        return self.data['RVDC'][name]

    # 油耗单位
    def get_avg_fuel(self, name):
        return self.data['UNIT_AVG_FUEL'][name]

    # 温度单位
    def get_unit_temperature(self, name):
        return self.data['UNIT_TEMPERATURE'][name]

    # 胎压单位
    def get_unit_tire_pressure(self, name):
        return self.data['UNIT_TIRE_PRESSURE'][name]

    # 距离单位
    def get_driven_distance(self, name):
        return self.data['DRIVEN_DISTANCE'][name]

    # 延时屏保
    def get_screen_saver_time(self, name):
        return self.data['SCREEN_SAVER_TIME'][name]

    # 时间制（24小时制，12小时制）
    def get_time_indication(self, name):
        return self.data['TIME_INDICATION'][name]

    # 年月日
    def get_date_frmat(self, name):
        return self.data['DATE_FORMAT'][name]

    # 手动尾门解锁 Manual_tailgate_unlock
    def get_manual_tailgate_unlock(self, name):
        return self.data['MANUAL_TAILGATE_UNLOCK'][name]

    # 外后视镜选择 REAR_MIRROR_ADJUST
    def get_rear_mirror_adjut(self, name):
        return self.data['REAR_MIRROR_ADJUST'][name]

    # 出风口10140100  REAR_MIRROR_ADJUST:
    def get_electrical_air_vent(self, name):
        return self.data['ELECTRICAL_AIR_VENT'][name]

    # 空调滤芯寿命重置
    def get_reset_filter_element_life(self, name):
        return self.data['RESET_FILTER_ELEMENT_LIFE'][name]

    # 自动启动空气净化器开关
    def get_auto_aac_swtich(self, name):
        return self.data['AUTO_AAC_SWITCH'][name]
        # 自动启动空气净化器开关

    def get_defrost_max(self, name):
        return self.data['DEFROST_MAX'][name]

    def get_auto_switch(self, name):
        return self.data['AUTO_SWITCH'][name]




    # # TSR自定义限速警告阈值（超速报警+-）
    # def get_speed_limit_warning_offset_value(self, name):
    #     return self.data['SPEED_LIMIT_WARNING_OFFSET_VALUE_MAX'][name]

###################################################################################################以下朱晓东
    # 弯道照明   lamp bendinglight
    def get_lamp_bendinglight(self, name):
        return self.data['LAMP_BENDINGLIGHT'][name]

    # 伴我回家灯   lamp home safe light
    def get_lamp_home_safe_light(self, name):
        return self.data['LAMP_HOME_SAFE_LIGHT'][name]

    # 近场灯   lamp approach light
    def get_lamp_approach_light(self, name):
        return self.data['LAMP_APPROACH_LIGHT'][name]

    # 后雾灯   light rear fog lamps
    def get_light_rear_fog_lamps(self, name):
        return self.data['LIGHT_REAR_FOG_LAMPS'][name]

    # 前雾灯   light front fog lamps
    def get_light_front_fog_lamps(self, name):
        return self.data['LIGHT_FRONT_FOG_LAMPS'][name]

    # 氛围灯空调联动      ambience_light_climate
    def get_ambience_light_climate(self, name):
        return self.data['AMBIENCE_LIGHT_CLIMATE'][name]

    # 氛围灯充电提醒         ambience_light_icharging_remind
    def get_ambience_light_icharging_remind(self, name):
        return self.data['AMBIENCE_LIGHT_ICHARGING_REMIND'][name]

    # 语音激活氛围灯       ambience_light_voice
    def get_ambience_light_voice(self, name):
        return self.data['AMBIENCE_LIGHT_VOICE'][name]

    # 方便主驾进出      easy_ingress_egress
    def get_easy_ingress_egress(self, name):
        return self.data['EASY_INGRESS_EGRESS'][name]

    # 眼球追踪      eye_ball_track
    def get_eye_ball_track(self, name):
        return self.data['EYE_BALL_TRACK'][name]

    # 一键休憩      seat_one_key_bed
    def get_seat_one_key_bed(self, name):
        return self.data['SEAT_ONE_KEY_BED'][name]

    # 第一排靠背调节      seat_backrest
    def get_seat_backrest(self, name):
        return self.data['SEAT_BACKREST'][name]

    # 座椅腰托前后调节      seat_lumbar_extended
    def get_seat_lumbar_extended(self, name):
        return self.data['SEAT_LUMBAR_EXTENDED'][name]

    # 座椅腰托上下调节      seat_lumbar_height
    def get_seat_lumbar_height(self, name):
        return self.data['SEAT_LUMBAR_HEIGHT'][name]

    #  多功能头枕上下调节     seat_headrest_height
    def get_seat_headrest_height(self, name):
        return self.data['SEAT_HEADREST_HEIGHT'][name]

    # 多功能头枕前后调节     seat_headrest_tilt
    def get_seat_headrest_tilt(self, name):
        return self.data['SEAT_HEADREST_TILT'][name]

    # 多功能第一排座垫延伸      seat_cushion_extension
    def get_seat_cushion_extension(self, name):
        return self.data['SEAT_CUSHION_EXTENSION'][name]

    # 座椅靠背侧翼支撑(前后)调节      seat_backrest_side_support
    def get_seat_backrest_side_support(self, name):
        return self.data['SEAT_BACKREST_SIDE_SUPPORT'][name]

    # 座椅座垫侧翼支撑高低(上下)调节    seat_cushion_side_support
    def get_seat_cushion_side_support(self, name):
        return self.data['SEAT_CUSHION_SIDE_SUPPORT'][name]

    # 预约出行开关      travel_appoint_charging
    def get_travel_appoint_charging(self, name):
        return self.data['TRAVEL_APPOINT_CHARGING'][name]

    # 预约空调    travel_hvac
    def get_travel_hvac(self, name):
        return self.data['TRAVEL_HVAC'][name]

    # 电池预热开关      warm_up
    def get_warm_up(self, name):
        return self.data['WARM_UP'][name]

    # 电池预热等级      warm_up_level
    def get_warm_up_level(self, name):
        return self.data['WARM_UP_LEVEL'][name]

    # 充电状态指示灯开关     external_charging_light
    def get_external_charging_light(self, name):
        return self.data['EXTERNAL_CHARGING_LIGHT'][name]

    # 发动机对外供电       external_power_supply
    def get_external_power_supply(self, name):
        return self.data['EXTERNAL_POWER_SUPPLY'][name]

    # 放电开关-V2V      discharging_switch_v2v
    def get_discharging_switch_v2v(self, name):
        return self.data['DISCHARGING_SWITCH_V2V'][name]

    # 放电开关-V2L      discharging_switch_v2l
    def get_discharging_switch_v2l(self, name):
        return self.data['DISCHARGING_SWITCH_V2L'][name]

    # 所有阅读灯        all_reading_lights_switch
    def get_all_reading_lights_switch(self, name):
        return self.data['ALL_READING_LIGHTS_SWITCH'][name]

    #  SayHi   lamp_say_hi
    def get_lamp_say_hi(self, name):
        return self.data['LAMP_SAY_HI'][name]

    # 第一排座椅按摩     seat_massage_switch
    def get_seat_massage_switch(self, name):
        return self.data['SEAT_MASSAGE_SWITCH'][name]

    # 插枪维温开关      maintain_battery_temp
    def get_maintain_battery_temp(self, name):
        return self.data['MAINTAIN_BATTERY_TEMP'][name]

    # 氛围灯驾驶模式联动      ambience_light_maincolor_drivermode
    def get_ambience_light_maincolor_drivermode(self, name):
        return self.data['AMBIENCE_LIGHT_MAINCOLOR_DRIVERMODE'][name]

    # 一键激活二排安全模式      rear_row_security_mode
    def get_rear_row_security_mode(self, name):
        return self.data['REAR_ROW_SECURITY_MODE'][name]

    # FusionSpeed     big_data_speed_limit
    def get_big_data_speed_limit(self, name):
        return self.data['BIG_DATA_SPEED_LIMIT'][name]

    # 座椅前后调节    seat_length
    def get_seat_length(self, name):
        return self.data['SEAT_LENGTH'][name]

    # 第一排座椅高度调节     seat_height
    def get_seat_height(self, name):
        return self.data['SEAT_HEIGHT'][name]

    # 一键进入仪式模式    lock_unlock_ceremony
    def get_lock_unlock_ceremony(self, name):
        return self.data['LOCK_UNLOCK_CEREMONY'][name]

    # 激活或关闭热石按摩功能    seat_hot_stone_massage
    def get_seat_hot_stone_massage(self, name):
        return self.data['SEAT_HOT_STONE_MASSAGE'][name]

    # 第二排腿托上下调节       seat_leg_support_height
    def get_seat_leg_support_height(self, name):
        return self.data['SEAT_LEG_SUPPORT_HEIGHT'][name]

    # 第二排腿托前后调节     seat_leg_support_length
    def get_seat_leg_support_length(self, name):
        return self.data['SEAT_LEG_SUPPORT_LENGTH'][name]

    #   变道警示LCA   lane_change_warning_mode
    def get_lane_change_warning_mode(self, name):
        return self.data['LANE_CHANGE_WARNING_MODE'][name]

    # 自动远光灯   lamp_active_high_beam_control
    def get_lamp_active_high_beam_control(self, name):
        return self.data['LAMP_ACTIVE_HIGH_BEAM_CONTROL'][name]

    # 格栅灯     light_grille_lamp_color
    def get_light_grille_lamp_color(self, name):
        return self.data['LIGHT_GRILLE_LAMP_COLOR'][name]

    # # 转向辅助灯(角灯)   lamp_cornering_light
    # def get_lamp_cornering_light(self, name):
    #     return self.data['LAMP_CORNERING_LIGHT'][name]

    # 方向盘转向力设置   steering assistance
    def get_steering_assistance(self, name):
        return self.data['STEERING_ASSISTANCE'][name]

    # 两步解锁
    def get_two_step_unlock(self, name):
        return self.data['TWO_STEP_UNLOCK'][name]

    # DOUBLE LOCK    double_lock
    def get_double_lock(self, name):
        return self.data['DOUBLE_LOCK'][name]

    # 驾驶员疲劳检测
    def get_driver_fatigue_detection(self, name):
        return self.data['DRIVER_FATIGUE_DETECTION'][name]

    # AEB自动紧急制动设置
    def get_autonomous_emergency_braking(self, name):
        return self.data['AUTONOMOUS_EMERGENCY_BRAKING'][name]

    # FCW 设定   forward_collision_warn_snvty   前碰撞预警灵敏等级
    def get_forward_collision_warn_snvty(self, name):
        return self.data['FORWARD_COLLISION_WARN_SNVTY'][name]

    # 后方碰撞警告RCW
    def get_rear_collision_warning(self, name):

        return self.data['REAR_COLLISION_WARNING'][name]

    # 车道保持辅助LKA   Lane keeping assistance
    def get_lane_keeping_assistance(self, name):
        return self.data['LANE_KEEPING_ASSISTANCE'][name]

    # 车道保持辅助模式开关 lane keeping aid mode
    def get_lane_keeping_aid_mode(self, name):
        return self.data['LANE_KEEPING_AID_MODE'][name]

    #  道保持辅助报警提示方式（声音，震动）  lane keeping aid warning 车道保持辅助警告类别
    def get_lane_keeping_aid_warning(self, name):
        return self.data['LANE_KEEPING_AID_WARNING'][name]

    # 转向避撞辅助系统EMA   emergency steering assist
    def get_emergency_steering_assist(self, name):
        return self.data['EMERGENCY_STEERING_ASSIST'][name]

    # 开车门预警DOW  door open warning
    def get_door_open_warning(self, name):
        return self.data['DOOR_OPEN_WARNING'][name]

    # 变道警示LCA-lotus lane change assist
    def get_lane_change_assist(self, name):
        return self.data['LANE_CHANGE_ASSIST'][name]

    # 变道辅助警报音开关  lane_change_assist_warning
    def get_lane_change_assist_warning(self, name):
        return self.data['LANE_CHANGE_ASSIST_WARNING'][name]

    #   后侧碰撞预警RCTA   rear cross traffic alert
    def get_rear_cross_traffic_alert(self, name):
        return self.data['REAR_CROSS_TRAFFIC_ALERT'][name]

    #   高速辅助HWA   auto lane change assist
    def get_auto_lane_change_assist(self, name):
        return self.data['AUTO_LANE_CHANGE_ASSIST'][name]

    # 自动辅助变道     drive_pilot
    def get_drive_pilot(self, name):
        return self.data['DRIVE_PILOT'][name]

    #   自适应巡航ACC TSR    acc with tsr
    def get_acc_with_tsr(self, name):
        return self.data['ACC_WITH_TSR'][name]

    #   交通标志识别TSI    traffic sign recognition
    def get_traffic_sign_recognition(self, name):
        return self.data['TRAFFIC_SIGN_RECOGNITION'][name]

    #   道路标志信息开关    Road Sign Information
    def get_road_sign_information(self, name):
        return self.data['ROAD_SIGN_INFORMATION'][name]

    #  限速信息提示选项   Speed limit warning mode
    def get_speed_limit_warning_mode(self, name):
        return self.data['SPEED_LIMIT_WARNING_MODE'][name]

    #  速度补偿   Speed limit warning offsettsr
    def get_speed_limit_warning_offsettsr(self, name):
        return self.data['SPEED_LIMIT_WARNING_OFFSETTSR'][name]

    # 交通灯提醒TLA   traffic light attention
    def get_traffic_light_attention(self, name):
        return self.data['TRAFFIC_LIGHT_ATTENTION'][name]

    # 交通灯报警设置开关   traffic light attention sound
    def get_traffic_light_attention_sound(self, name):
        return self.data['TRAFFIC_LIGHT_ATTENTION_SOUND'][name]

    # 应急车道占用提醒 ELOW    Emergency lane occupancy reminder
    def get_emergency_lane_occupancy_reminder(self, name):
        return self.data['EMERGENCY_LANE_OCCUPANCY_REMINDER'][name]

    # 中控锁      central lock
    def get_central_lock(self, name):
        return self.data['CENTRAL_LOCK'][name]

    # 上锁音声反馈      Locking sound feedback   可听落锁反馈
    def get_locking_sound_feedback(self, name):
        return self.data['LOCKING_SOUND_FEEDBACK'][name]

    # 靠近解锁      approach unlock   接近解锁
    def get_approach_unlock(self, name):
        return self.data['APPROACH_UNLOCK'][name]

    # 解锁车门方式      keyless unlocking   无钥匙解锁设置
    def get_keyless_unlocking(self, name):
        return self.data['KEYLESS_UNLOCKING'][name]

    # 锁车视镜自动折叠 主驾驶     mirror auto folding   外后视镜自动折叠
    def get_mirror_auto_folding(self, name):
        return self.data['MIRROR_AUTO_FOLDING'][name]

    # 一键后视镜折叠   fold rear mirror
    def get_fold_rear_mirror(self, name):
        return self.data['FOLD_REAR_MIRROR'][name]

    # 阅读灯  light reading light
    def get_light_reading_light(self, name):
        return self.data['LIGHT_READING_LIGHT'][name]

    # HUD 开关 可用性   hud active
    def get_hud_active(self, name):
        return self.data['HUD_ACTIVE'][name]

    # HUD 亮度设置 HUD brightness
    def get_hud_brightness(self, name):
        return self.data['HUD_BRIGHTNESS'][name]

    # HUD 角度调节 HUD angle adjust
    def get_hud_angle_adjust(self, name):
        return self.data['HUD_ANGLE_ADJUST'][name]

    # HUD 雪地模式 HUD snow mode
    def get_hud_snow_mode(self, name):
        return self.data['HUD_SNOW_MODE'][name]

    # HUD AR 开关 HUD AR engine
    def get_hud_ar_engine(self, name):
        return self.data['HUD_AR_ENGINE'][name]

    # # 空调总开关   climate power
    # def get_climate_power(self, name):
    #     return self.data['CLIMATE_POWER'][name]

    # # AC    havc func ac
    # def get_havc_func_ac(self, name):
    #     return self.data['HAVC_FUNC_AC'][name]

    # 温度双区同步  hvac temp dual
    def get_hvac_temp_dual(self, name):
        return self.data['HVAC_TEMP_DUAL'][name]

    # # 温度控制控制   HAVC_FUNC_TEMP
    # def get_havc_func_temp(self, name):
    #     return self.data['HAVC_FUNC_TEMP'][name]

    # 驻车空调 调节功能 hvac pre climatisation
    def get_havc_pre_climatisation(self, name):
        return self.data['HAVC_PRE_CLIMATISATION'][name]

    # 驻车空调 加热功能 hvac post climatisation
    def get_havc_post_climatisation(self, name):
        return self.data['HAVC_POST_CLIMATISATION'][name]

    # 前排电除霜   hvac  defrost front
    def get_hvac_defrost_front(self, name):
        return self.data['HVAC_DEFROST_FRONT'][name]

    # 后排电除霜   hvac  defrost rear
    def get_hvac_defrost_rear(self, name):
        return self.data['HVAC_DEFROST_REAR'][name]

    #  座椅加热挡位 hvac seat heating
    def get_hvac_seat_heating(self, name):
        return self.data['HVAC_SEAT_HEATING'][name]

    #  座椅加热时间  hvac auto seat heating time
    def get_hvac_auto_seat_heating_time(self, name):
        return self.data['HVAC_AUTO_SEAT_HEATING_TIME'][name]

    # '''座椅通风档位'''
    # def get_havc_seat_vent_level(self, name):
    #     return self.data['HAVC_SEAT_VENT_LEVEL'][name]

    # '''座椅通风时间'''
    # def get_havc_auto_seat_vent_time(self, name):
    #     return self.data['HAVC_AUTO_SEAT_VENT_TIME'][name]

    # 顶灯  ambience light topzones
    def get_ambience_light_topzones(self, name):
        return self.data['AMBIENCE_LIGHT_TOPZONES'][name]

    # 氛围灯总开关  light atmosphere lamps
    def get_light_atmosphere_lamps(self, name):
        return self.data['LIGHT_ATMOSPHERE_LAMPS'][name]

    # 门控灯  lamp automatic courtesy light
    def get_lamp_automatic_courtesy_light(self, name):
        return self.data['LAMP_AUTOMATIC_COURTESY_LIGHT'][name]

    # 氛围灯 音乐模式  ambience light music show mode
    def get_ambience_light_music_show_mode(self, name):
        return self.data['AMBIENCE_LIGHT_MUSIC_SHOW_MODE'][name]

    # 续航里程灯  ambience light endurance mil reminder
    def get_ambience_light_endurance_mil_reminder(self, name):
        return self.data['AMBIENCE_LIGHT_ENDURANCE_MIL_REMINDER'][name]

    # 送别灯  ambience light goodbye show
    def get_ambience_light_goodbye_show(self, name):
        return self.data['AMBIENCE_LIGHT_GOODBYE_SHOW'][name]

    # 氛围灯模式   ambience light maincolor
    def get_ambience_light_maincolor(self, name):
        return self.data['AMBIENCE_LIGHT_MAINCOLOR'][name]

    # 欢迎灯开关  ambience light welconme show
    def get_ambience_light_welconme_show(self, name):
        return self.data['AMBIENCE_LIGHT_WELCOME_SHOW'][name]

    # 欢迎氛围灯模式设置   ambience light welconme show mode
    def get_ambience_light_welconme_show_mode(self, name):
        return self.data['AMBIENCE_LIGHT_WELCOME_SHOW_MODE'][name]

    # LDAC      life detection
    def get_life_detection(self, name):
        return self.data['LIFE_DETECTION'][name]

    # AI辅助驾驶开关  ai_driver_assist
    def get_ai_driver_assist(self, name):
        return self.data['AI_DRIVER_ASSIST'][name]

    # 变道需确认开关  ai_assist_lane_change_confirm
    def get_ai_assist_lane_change_confirm(self, name):
        return self.data['AI_ASSIST_LANE_CHANGE_CONFIRM'][name]

    # 变道提醒选项   ai_assist_lane_change_warning
    def get_ai_assist_lane_change_warning(self, name):
        return self.data['AI_ASSIST_LANE_CHANGE_WARNING'][name]

    # 变道策略   ai_assist_lane_change_strategy
    def get_ai_assist_lane_change_strategy(self, name):
        return self.data['AI_ASSIST_LANE_CHANGE_STRATEGY'][name]

    # 让出超车道开关   ai_assist_out_overtaking_lane
    def get_ai_assist_out_overtaking_lane(self, name):
        return self.data['AI_ASSIST_OUT_OVERTAKING_LANE'][name]

    # 融合导航开关   ai_assist_fusion_navi
    def get_ai_assist_fusion_navi(self, name):
        return self.data['AI_ASSIST_FUSION_NAVI'][name]

    # 上电默认开开关    ai_assist_default_on
    def get_ai_assist_default_on(self, name):
        return self.data['AI_ASSIST_DEFAULT_ON'][name]

    # 乘客安全气囊   passenger_airbag
    def get_passenger_airbag(self, name):
        return self.data['PASSENGER_AIRBAG'][name]

    # 纯电续航里程显示方式设置   electric_mileage_display_switch
    def get_electric_mileage_display_switch(self, name):
        return self.data['ELECTRIC_MILEAGE_DISPLAY_SWITCH'][name]

    # 流媒体后视镜    ele_mirror_sys_activated
    def get_ele_mirror_sys_activated(self, name):
        return self.data['ELE_MIRROR_SYS_ACTIVATED'][name]

    # 等人模式      waiting_mode
    def get_waiting_mode(self, name):
        return self.data['WAITING_MODE'][name]

    # 欢迎送别灯模式设置       welcome_light_mode
    def get_welcome_light_mode(self, name):
        return self.data['WELCOME_LIGHT_MODE'][name]

    # 旅行灯L/RSetup     lamp_lr_traffic_light
    def get_lamp_lr_traffic_light(self, name):
        return self.data['LAMP_LR_TRAFFIC_LIGHT'][name]

    # 自适应巡航灯    lamp_adaptive_front_light
    def get_lamp_adaptive_front_light(self, name):
        return self.data['LAMP_ADAPTIVE_FRONT_LIGHT'][name]

    # 电动门自动开门      auto_power_door
    def get_auto_power_door(self, name):
        return self.data['AUTO_POWER_DOOR'][name]

    # 驾驶舱过热保护     overheat_protection
    def get_overheat_protection(self, name):
        return self.data['OVERHEAT_PROTECTION'][name]

    # 自动后雨刮     auto rear wiping
    def get_auto_rear_wiping(self, name):
        return self.data['AUTO_REAR_WIPING'][name]

    # 车内模拟声浪开关    artificial sound switch
    def get_artificial_sound_switch(self, name):
        return self.data['ARTIFICIAL_SOUND_SWITCH'][name]

    # 超速报警开关     speed limit warning offset value switch
    def get_speed_limit_warning_offset_value_switch(self, name):
        return self.data['SPEED_LIMIT_WARNING_OFFSET_VALUE_SWITCH'][name]

    # 方向盘角度报警开关          steering wheel angle warn switch
    def get_steering_wheel_angle_warn_switch(self, name):
        return self.data['STEERING_WHEEL_ANGLE_WARN_SWITCH'][name]

    # 运动模式      drive mode selection dynamic
    def get_drive_mode_selection_dynamic(self, name):
        return self.data['DRIVE_MODE_SELECTION_DYNAMIC'][name]

    # # 驾驶模式之舒适模式
    # def get_drive_mode_selection_comfort(self, name):
    #     return self.data['DRIVE_MODE_SELECTION_COMFORT'][name]

    # 驾驶模式之混动模式    drive mode selection hybrid
    def get_drive_mode_selection_hybrid(self, name):
        return self.data['DRIVE_MODE_SELECTION_HYBRID'][name]

    # 驾驶模式之动力模式    drive mode selection power
    def get_drive_mode_selection_power(self, name):
        return self.data['DRIVE_MODE_SELECTION_POWER'][name]


readConfig = ReadConfig()
